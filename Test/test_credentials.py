def verificar(idv,secretv): 
    idver = "Dados"
    secver = "DadosSecret"
    if(idv==idver and secver==secretv):
        return True
    else:
        return False

def test_credentials():
    assert verificar("Dados","DadosSecret")==True