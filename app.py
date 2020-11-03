import json
import jwt
import datetime
import pymongo
from autenticacion import token_required, verificar # The token verification script
from flask import Flask, request, Response, json
from flask_cors import CORS
private_key = b'''-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAnzyis1ZjfNB0bBgKFMSvvkTtwlvBsaJq7S5wA+kzeVOVpVWw
kWdVha4s38XM/pa/yr47av7+z3VTmvDRyAHcaT92whREFpLv9cj5lTeJSibyr/Mr
m/YtjCZVWgaOYIhwrXwKLqPr/11inWsAkfIytvHWTxZYEcXLgAXFuUuaS3uF9gEi
NQwzGTU1v0FqkqTBr4B8nW3HCN47XUu0t8Y0e+lf4s4OxQawWD79J9/5d3Ry0vbV
3Am1FtGJiJvOwRsIfVChDpYStTcHTCMqtvWbV6L11BWkpzGXSW4Hv43qa+GSYOD2
QU68Mb59oSk2OB+BtOLpJofmbGEGgvmwyCI9MwIDAQABAoIBACiARq2wkltjtcjs
kFvZ7w1JAORHbEufEO1Eu27zOIlqbgyAcAl7q+/1bip4Z/x1IVES84/yTaM8p0go
amMhvgry/mS8vNi1BN2SAZEnb/7xSxbflb70bX9RHLJqKnp5GZe2jexw+wyXlwaM
+bclUCrh9e1ltH7IvUrRrQnFJfh+is1fRon9Co9Li0GwoN0x0byrrngU8Ak3Y6D9
D8GjQA4Elm94ST3izJv8iCOLSDBmzsPsXfcCUZfmTfZ5DbUDMbMxRnSo3nQeoKGC
0Lj9FkWcfmLcpGlSXTO+Ww1L7EGq+PT3NtRae1FZPwjddQ1/4V905kyQFLamAA5Y
lSpE2wkCgYEAy1OPLQcZt4NQnQzPz2SBJqQN2P5u3vXl+zNVKP8w4eBv0vWuJJF+
hkGNnSxXQrTkvDOIUddSKOzHHgSg4nY6K02ecyT0PPm/UZvtRpWrnBjcEVtHEJNp
bU9pLD5iZ0J9sbzPU/LxPmuAP2Bs8JmTn6aFRspFrP7W0s1Nmk2jsm0CgYEAyH0X
+jpoqxj4efZfkUrg5GbSEhf+dZglf0tTOA5bVg8IYwtmNk/pniLG/zI7c+GlTc9B
BwfMr59EzBq/eFMI7+LgXaVUsM/sS4Ry+yeK6SJx/otIMWtDfqxsLD8CPMCRvecC
2Pip4uSgrl0MOebl9XKp57GoaUWRWRHqwV4Y6h8CgYAZhI4mh4qZtnhKjY4TKDjx
QYufXSdLAi9v3FxmvchDwOgn4L+PRVdMwDNms2bsL0m5uPn104EzM6w1vzz1zwKz
5pTpPI0OjgWN13Tq8+PKvm/4Ga2MjgOgPWQkslulO/oMcXbPwWC3hcRdr9tcQtn9
Imf9n2spL/6EDFId+Hp/7QKBgAqlWdiXsWckdE1Fn91/NGHsc8syKvjjk1onDcw0
NvVi5vcba9oGdElJX3e9mxqUKMrw7msJJv1MX8LWyMQC5L6YNYHDfbPF1q5L4i8j
8mRex97UVokJQRRA452V2vCO6S5ETgpnad36de3MUxHgCOX3qL382Qx9/THVmbma
3YfRAoGAUxL/Eu5yvMK8SAt/dJK6FedngcM3JEFNplmtLYVLWhkIlNRGDwkg3I5K
y18Ae9n7dHVueyslrb6weq7dTkYDi3iOYRW8HRkIQh06wEdbxt0shTzAJvvCQfrB
jg/3747WSsf/zBTcHihTRBdAv6OmdhV4/dD5YBfLAkLrd+mX7iE=
-----END RSA PRIVATE KEY-----'''

app = Flask(__name__)
CORS(app)
client = pymongo.MongoClient("mongodb://mongosrv:27017")
db = client["Tokens"]
collection = db["Scope"]
Log = open("LogTokens.txt","w")

@app.route('/token', methods=['POST'])
def loginFunction():
    idusr = request.args.get("id")
    secret = request.args.get("secret")
    myquery = {"idService":idusr}
    x = collection.find(myquery)
    
    if (verificar(idusr,secret)==True):
        timeLimit= datetime.datetime.utcnow() + datetime.timedelta(minutes=30) #set limit for user
        playload = {"alg":"RS256",
            "typ":"JWT",
            "exp":timeLimit, 
            "scope":dict(x[0]).get("scope")
        }
        
        token_bytes = jwt.encode(playload, private_key, algorithm = 'RS256')
        return_data={
            "jwt": token_bytes.decode('utf-8'),
        }
        print("Token: ", str(return_data)," COD: 200;")
        Log.write("Token: ", str(return_data)," COD: 200;"+"\n")
        return app.response_class(response=json.dumps(return_data), mimetype='application/json')
    else:
        err = {
            'error':"credenciales no validas"
        }
        print("Token: ", str(err)," COD: 403;")
        Log.write("Token: ", str(err)," COD: 403;"+"\n")
        return app.response_class(response=json.dumps(err), mimetype='application/json')

@app.route('/anEndpoint',methods=['POST'])
@token_required #Verify token decorator
def aWebService():
    return_data = {
        "error": "0",
        "message": "You Are verified"
        }
    return app.response_class(response=json.dumps(return_data), mimetype='application/json')


@app.route('/', methods=['GET'])
def index():
    res = {'Status': 'Successfully ' + 'request ok'}
    return Response(response=json.dumps(res),
                    status=200,
                    mimetype='application/json')

if __name__ == "__main__":
    app.run(port=5001, debug=True, host='0.0.0.0')
