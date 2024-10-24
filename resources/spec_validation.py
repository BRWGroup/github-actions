def validate_data_product_spec():
    try:
        if 1 == 2:
            raise Exception("Wowowwow")
    except:
        return False
    
    return True


print(f'::set-output name=validity::{validate_data_product_spec()}')