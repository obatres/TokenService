def registro(x):
    if x!=[] and x!= None:
        return True
    else:
        return False

def test_registro():
    x = ['service.metodo']
    assert registro(x)==True