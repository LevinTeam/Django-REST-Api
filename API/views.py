from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import api_view, throttle_classes
import json
import base64
from .models import CommentsData, Users
# Create your views here.

@api_view(['POST'])
@throttle_classes([UserRateThrottle])
def commentHandler(request):
    ReceivedData = json.loads(request.body.decode('utf-8'))['CommentData']
    if request.method == 'POST' and request.content_type == 'application/json':
        if str(ReceivedData['name']) and len(ReceivedData['name']) <= 40:
            if str(ReceivedData['email']) and ReceivedData['email'].isascii() and (ValidateEmail(ReceivedData['email'], '@gmail.com') or ValidateEmail(ReceivedData['email'], '@yahoo.com') or ValidateEmail(ReceivedData['email'], '@outlook.com')):
                if str(ReceivedData['phone']):
                    if len(ReceivedData['phone']) == 11 or len(ReceivedData['phone']) == 12:
                        if ValidatePhoneNumber(ReceivedData['phone'], '09') or ValidatePhoneNumber(ReceivedData['phone'], '98'):
                            if str(ReceivedData['subject']):
                                if len(ReceivedData['subject']) > 5:
                                    if len(ReceivedData['subject']) < 40:
                                        if str(ReceivedData['message']):
                                            if len(ReceivedData['message']) > 20:
                                                if len(ReceivedData['message']) < 500:
                                                    CommentsData.objects.create(name=ReceivedData['name'], email=ReceivedData['email'], phone=ReceivedData['phone'], subject=ReceivedData['subject'], message=ReceivedData['message'])
                                                    return ApiResponse(201,'Created', 'نظر شما با موفقیت ثبت شد و برای ادمین های ما ارسال شد')
                                                else:
                                                    return ApiResponse(400, 'Bad Request: Comment should be smaller than 500 characters')
                                            else:
                                                return ApiResponse(400,'Bad Request: Comment should be larger than 20 characters')
                                        else:
                                            return ApiResponse(400,'Bad Request: Comment must be string')
                                    else:
                                        return ApiResponse(400,'Bad Request: Subject should be smaller than 40 characters')
                                else:
                                    return ApiResponse(400, 'Bad Request: Subject should be larger than 5 characters')
                            else:
                                return ApiResponse(400, 'Bad Request: Subject must be string')
                        else:
                            return ApiResponse(400, 'Bad Request: Invalid phone number type')
                    else:
                        return ApiResponse(400, 'Bad Request: Invalid phone number length')
                else:
                    return ApiResponse(400, 'Bad Request: Phone number must be string')
            else:
                return ApiResponse(400, 'Bad Request: Invalid Email type')
        else:
            return ApiResponse(400, 'Bad Request: Invalid name type')
    else:
        return ApiResponse(405, 'Method Not Allowed')


@api_view(['POST', 'GET'])
@throttle_classes([UserRateThrottle])
def userHandler(request):
    ReceivedData = json.loads(request.body.decode('utf-8'))['UserData']
    EncryptPassword = base64.b64encode(ReceivedData['password'].encode('utf-8'))
    DecryptPassword = base64.b64decode(EncryptPassword.decode('utf-8').encode('utf-8'))
    print(ReceivedData, '\n\n\n')

    if (request.method == 'POST' and request.content_type == 'application/json') or (request.method == 'GET' and request.content_type == 'application/json'):
        if Users.objects.filter(email=ReceivedData['email']).exists():
            if str(ReceivedData['email']) and ReceivedData['email'].isascii() and (ValidateEmail(ReceivedData['email'], '@gmail.com') or ValidateEmail(ReceivedData['email'],'@yahoo.com') or ValidateEmail(ReceivedData['email'], '@outlook.com')):
                if Users.objects.get(email=ReceivedData['email']).email == ReceivedData['email']:
                    if str(ReceivedData['password']) and ReceivedData['password'].isascii():
                        if (Users.objects.get(email=ReceivedData['email']).password) == EncryptPassword.decode('utf-8'):
                            return ApiResponse(200, 'Successful Login', f'hello {Users.objects.get(email=ReceivedData['email']).firstname} {Users.objects.get(email=ReceivedData['email']).lastname}, You Have Been Logined Successfully into your account')
                        else:
                            return ApiResponse(400, 'Bad Request: Wrong Password')
                    else:
                        return ApiResponse(400, 'Bad Request: Invalid Password Type')
                else:
                    return ApiResponse(400, 'Bad Request: Wrong Email')
            else:
                return ApiResponse(400, 'Bad Request: Invalid Email type')
        else:
            if str(ReceivedData['firstname']) and len(ReceivedData['firstname']) <= 40:
                if str(ReceivedData['lastname']) and len(ReceivedData['lastname']) <= 40:
                    if str(ReceivedData['email']) and ReceivedData['email'].isascii() and (ValidateEmail(ReceivedData['email'], '@gmail.com') or ValidateEmail(ReceivedData['email'], '@yahoo.com') or ValidateEmail(ReceivedData['email'], '@outlook.com')):
                        if str(ReceivedData['phone']):
                            if len(ReceivedData['phone']) == 11 or len(ReceivedData['phone']) == 12:
                                if ValidatePhoneNumber(ReceivedData['phone'], '09') or ValidatePhoneNumber(ReceivedData['phone'], '98'):
                                    if str(ReceivedData['password']) and ReceivedData['password'].isascii():
                                        Users.objects.create(firstname=ReceivedData['firstname'], lastname=ReceivedData['lastname'], email=ReceivedData['email'], phone=ReceivedData['phone'], password=EncryptPassword.decode('utf-8'))
                                        return ApiResponse(201, 'Created', 'Your account has been created')
                                    else:
                                        return ApiResponse(400, 'Bad Request: Invalid Password Type')
                                else:
                                    return ApiResponse(400, 'Bad Request: Invalid phone number type')
                            else:
                                return ApiResponse(400, 'Bad Request: Invalid phone number length')
                        else:
                            return ApiResponse(400, 'Bad Request: Phone number must be string')
                    else:
                        return ApiResponse(400, 'Bad Request: Invalid Email type')
                else:
                    return ApiResponse(400, 'Bad Request: Invalid lastname type')
            else:
                return ApiResponse(400, 'Bad Request: Invalid firstname type')
    else:
        return ApiResponse(405, 'Method Not Allowed')

def ValidateEmail(EmailAddress, Sign):
    return EmailAddress.__contains__(Sign)

def ValidatePhoneNumber(PhoneNumber, Sign):
    return PhoneNumber.startswith(Sign)

def ApiResponse(statusCode, statusMessage, message="null message"):
    return Response({
        'message': message,
        'status': {
            'code': statusCode,
            'message': statusMessage
        }
    })
