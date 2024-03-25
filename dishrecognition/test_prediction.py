from prediction import predict_dish, create_foodlist
from tensorflow.keras.models import load_model

my_model = load_model('model_trained.h5', compile = False)

def test_predict_dish():
    assert predict_dish(my_model, '../dataset/manual_test/caesar.jpg') == 'caesar_salad'
    assert predict_dish(my_model, '../dataset/manual_test/creme.jpeg') == 'creme_brulee'
    assert predict_dish(my_model, '../dataset/manual_test/oignon.jpeg') == 'french_onion_soup'
    assert predict_dish(my_model, '../dataset/manual_test/pizza.jpeg') == 'pizza'
    
def test_create_foodlist():
    food_list = create_foodlist('../dataset/images')
    food_list.sort()
    assert food_list[0] == 'apple_pie'
    assert food_list[100] == 'waffles'
     