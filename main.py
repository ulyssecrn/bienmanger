from flask import Flask, render_template, flash, redirect, url_for, request, session
from werkzeug.utils import secure_filename
import os
from dishrecognition.prediction import predict_dish
from tensorflow.keras.models import load_model
from deep_translator import GoogleTranslator
from api import id_recipe, nutriscore_recipe, wine_pairing,nutriscore_color

#   Création de l'aplication web

app = Flask(__name__)
app.template_folder = 'web/templates'
app.static_folder = 'web/assets'
app.secret_key= '8b3a3a11f5cfbc97ab03027611f2574909d20bdb2fcbac1efcf31312bc222e9e'

#   Load the prediction model

my_model = load_model('dishrecognition/model_trained.h5', compile = False)


#   Test if the data is an image

def allowed_file(filename):
    return '.' in filename and (filename.rsplit('.', 1)[1].lower() in ['jpg', 'jpeg', 'png'])

#   Define the routes taken when the user interacts with the web application

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('siteweb.html')

@app.route('/recette/<name>', methods=['GET','POST'])
def recette(name):
    return render_template('recette.html', recetteName = name)

@app.route('/chercher', methods=['POST'])
def chercher():
    
    if 'recipeImage' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['recipeImage']
    
    if file.filename == '':
        flash('Aucun fichier n\'a été sélectionné')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join('web/submitted_data/', filename)
        file.save(path)
        prediction = predict_dish(my_model, path)
        recipe_name_en = prediction.replace('_', ' ')
        recipe_name = GoogleTranslator(source='en', target='fr').translate(recipe_name_en)
        
        try:
            id_recip=id_recipe(recipe_name_en)
            session['nutriscore']=nutriscore_recipe(id_recip)
            wine_text_name= wine_pairing(recipe_name_en)
            session['wine_text']= wine_text_name[0]
            session['wine_name']= wine_text_name[1]
        except:
            session['nutriscore']='pas encore défini'
            session['wine_text']= 'pas encore de vin'
            session['wine_name']= ''
        finally:
            session['color']=nutriscore_color(session['nutriscore'])
            os.remove(path) # Delete the file saved in submitted_data
            return redirect(url_for('recette', name=recipe_name))





if __name__ == "__main__":
    app.run(port=8080)
