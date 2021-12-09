
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages

import re
import bcrypt

from app1.models import user, amigos

from datetime import datetime, time, timezone
from time import gmtime, strftime



EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

def index(request):
    if 'login' not in request.session:
        request.session['login'] = False
    
    if 'u_id' not in request.session:
        request.session['u_id'] = 0
    return render(request, 'index.html')

def registro(request):

    check = user.objects.filter(email = request.POST['email'])
    
    error = False
    

    if len(request.POST['name'])< 3:
        messages.error(request,'Tu nombre debe tener al menos 3 carácteres.', extra_tags = 'fn_error' )
        error = True

    if len(request.POST['alias'])< 3:
        messages.error(request,'Tu alias debe tener al menos 3 carácteres.', extra_tags = 'ln_error')
        error = True
    
    if check:
        messages.error(request,'Este email ya se encuentra registrado', extra_tags = 'email_error')
        error = True

    # PASSWORD, CONFIRM PASSWORD 

    if request.POST['password'] != request.POST['confirm_password']:
        messages.error(request,'Las contraseñas no coinciden', extra_tags = 'pw_error')
        error = True

    if len(request.POST['password']) < 8 :
        messages.error(request,'Tu contraseña debe teener al menos 8 carácteres', extra_tags = 'pw_error')
        error = True

    # =======================================

    if error == True:
        return redirect('/')

    elif error == False:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = user.objects.create(name = request.POST['name'], alias = request.POST['alias'],email=request.POST['email'], day_of_birth=request.POST['date_of_birthday'], password = pw_hash)
        print(new_user)
        request.session['user_id'] = new_user.id
        # save User._id in session
        messages.success(request, 'Te has registrado exitosamente. ¡Ya puedes iniciar sesión!', extra_tags = 'registered')
        
        return redirect('/')

def login(request):
    email = request.POST["email"]
    password = request.POST["password"]
    print(f"{email} {password}")
    echeck = user.objects.filter(email=email) 
    print (echeck)
    if echeck:
        print('EXISTE EMAIL')
        if bcrypt.checkpw(request.POST['password'].encode(), echeck[0].password.encode()):
            print(echeck[0].password)
            request.session['login'] = True
            request.session['u_id'] = echeck[0].id
            userss=user.objects.get(id=request.session['u_id'])
            amiguito=amigos.objects.create(llave=userss)
            # POSIBLE ERROR
            amiguito.friends.add(userss)
            # REVISAR LUEGO =======********
            return redirect('/friends')
        else:
            print('CONTRASEÑA INCORRECTA')
            messages.error(request,'Contraseña incorrecta', extra_tags = 'mal_login_pass_dato')
            return redirect('/')

    else: 
        messages.error(request,'Email No registrado', extra_tags = 'mal_dato_login_e')
        return redirect('/')

def friends(request):
    print('INGRESO AL DASHBOARD FRIENDS')
    if request.session['login'] == True:
        user_1 = user.objects.get(id = request.session['u_id'])
        # user_info = {
        #     'user': user_1[0]
        # }
        # print(user_info['user'])
        context={
            'usuarios': user.objects.all(),
            'amigoss': amigos.objects.all(),
            'user': user_1,
        }
        # print("*"*10)
        # print(context['amigoss'])
        # print(context['usuarios'])
        # print("*"*10)
        return render(request, 'allFriends.html', context)
    else:
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def userProfile(request,id):
    context={
        'amigos':user.objects.get(id=id)
    }
    return render(request, 'userProfile.html', context)


# ==== TRABAJANDO

def addFriend(request,id):

    new_amigos=amigos.objects.get(id=id)
    session_id_login=user.objects.get(id=request.session['u_id'])

    # AGREGO "NEW_AMIGOS" A LA LISTA DE AMIGOS DE "SESSION_ID_LOGIN"
    new_amigos.friends.add(session_id_login)

    new_amigos.save()

    return redirect('/friends')


def remove(request, id):
    new_amigos=amigos.objects.get(id=id)
    session_id_login=user.objects.get(id=request.session['u_id'])

    # REMUEVO "NEW_AMIGOS" DE LA LISTA DE AMIGOS DE "SESSION_ID_LOGIN"
    new_amigos.friends.remove(session_id_login)

    new_amigos.save()

    return redirect('/friends')
