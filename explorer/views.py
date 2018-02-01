from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from explorer.models import Question
from explorer.models import Answer
from explorer.models import Follow
from explorer.models import Like


# Create your views here.
@login_required
#问题页面
def getlist(request):
        quelist = Question.objects.all()
        quelist_2=Question.objects.order_by('-answernum')[0:3]
        user = request.user.username
        return render(request, 'question.html', {'quelist_2': quelist_2, 'quelist': quelist, 'username': user})

@login_required
#用户页面
def user_view(request):
    if request.method == 'GET':
        name= request.GET['username']
        user=User.objects.get(username=name)
        quelist=Question.objects.filter(questioner=name)  #有用
        answerlist=Answer.objects.filter(answername=name)
        followlist=Follow.objects.filter(userid=user)
        followque=[]
        for onefollow in followlist:
            temp=Question.objects.get(id=onefollow.questionid)
            followque.append(temp)
        anslist=[]
        que=[]
        for oneswer in answerlist:
            que.append(Question.objects.get(id=oneswer.questionid))
        for temp1,temp2 in zip(que,answerlist):
            temp = {'id':temp1.id,'questionname':temp1.questionname,'answercontent':temp2.content}
            anslist.append(temp)
        return render(request, 'user.html',{'quelist':quelist,'anslist':anslist,'user':user,'followque':followque})

@login_required
#答案页面
def answer_view(request):
    if request.method == 'GET':
        questionid=request.GET['nomalid']
        onequestion=Question.objects.get(id=questionid)
        answerlist=Answer.objects.filter(questionid=questionid)
        answername=request.user.username
        anslist=[]
        likelist=[]
        for temp in answerlist:
            one=Like.objects.filter(answerid=temp.id,userid=answername)
            if len(one)==0: #没有点赞
                onelike=0
            else:
                onelike = 1
            likelist.append(onelike)
        for x,y in zip(answerlist,likelist):
            temptwo={'id':x.id,'content':x.content,'questionid':x.questionid,'answername':x.answername,'likenum':x.likenum,'flag':y}
            anslist.append(temptwo)
        follow=Follow.objects.filter(questionid=questionid, userid=answername)
        if len(follow)==0:
            isfollow=0
        else:
            isfollow=1
        return render(request, 'answer.html',{'onequestion':onequestion,'answerlist':anslist,'answername':answername,'isfollow':isfollow})

@login_required
#用户进入页面
def answeruserview(request):
    if request.method == 'GET':
        questionid=request.GET['nomalid']
        onequestion=Question.objects.get(id=questionid)
        onequestion.remind=0
        onequestion.save()
        answerlist=Answer.objects.filter(questionid=questionid)
        answername=request.user.username
        anslist=[]
        likelist=[]
        for temp in answerlist:
            one=Like.objects.filter(answerid=temp.id,userid=answername)
            if len(one)==0: #没有点赞
                onelike=0
            else:
                onelike = 1
            likelist.append(onelike)
        for x,y in zip(answerlist,likelist):
            temptwo={'id':x.id,'content':x.content,'questionid':x.questionid,'answername':x.answername,'likenum':x.likenum,'flag':y}
            anslist.append(temptwo)
        follow=Follow.objects.filter(questionid=questionid, userid=answername)
        if len(follow)==0:
            isfollow=0
        else:
            isfollow=1
        return render(request, 'answer.html',{'onequestion':onequestion,'answerlist':anslist,'answername':answername,'isfollow':isfollow})

@login_required
#添加回答
def answer_add(request):
    username = request.POST['answername']
    content1 = request.POST['ansContent']
    questionid= request.POST['questionid']
    onequestion = Question.objects.get(id=questionid)
    onequestion.answernum+=1
    onequestion.remind+=1
    onequestion.save()
    newanswer = Answer(content=content1,questionid=questionid,answername=username,likenum=0)
    newanswer.save()
    res = {"success": "true"}
    return JsonResponse(res)

@login_required
#添加问题
def question_add(request):
    username=request.POST['username']
    questionname1=request.POST['quesHead']
    content1=request.POST['quesContent']
    newquestion = Question(questionname=questionname1, content=content1, answernum=0,questioner=username,remind=0)
    newquestion.save()
    res = {"success": "true"}
    return JsonResponse(res)

@login_required
def todogetlist(request):
    dataset = Question.objects.all()
    questionlist=[]
    for item in dataset:
        temp = {"id": item.id, "content": item.content,"questionname":item.questionname,"answernum":item.answernum}
        questionlist.append(temp)
    res = {"questionlist": questionlist}
    return JsonResponse(res)

@login_required
def answerlist(request):
    questionid=request.GET['questionid']
    dataset = Answer.objects.filter(questionid=questionid)
    anslist=[]
    likelist = []
    for temp in dataset:
        one = Like.objects.filter(answerid=temp.id, userid=request.user.username)
        if len(one) == 0:  # 没有点赞
            onelike = 0
        else:
            onelike = 1
        likelist.append(onelike)
    for x, y in zip(dataset, likelist):
        temptwo = {'id': x.id, 'content': x.content, 'questionid': x.questionid, 'answername': x.answername,
                   'likenum': x.likenum, 'flag': y}
        anslist.append(temptwo)
    res = {"answerlist":anslist}
    return JsonResponse(res)

@login_required
#关注处理
def followexe(request):
    questionid=request.POST['questionid']
    username=request.POST['answername']
    f=Follow(questionid=questionid,userid=username)
    f.save()
    res = {"success": "true"}
    return JsonResponse(res)

@login_required
#取消关注处理
def unfollowexe(request):
    questionid = request.POST['questionid']
    username = request.POST['answername']
    Follow.objects.get(questionid=questionid,userid=username).delete()
    res = {"success": "true"}
    return JsonResponse(res)

@login_required
#点赞处理
def likeexe(request):
    id=request.POST['id']
    onelike=Like(answerid=id,userid=request.user.username)
    onelike.save()
    oneanswer=Answer.objects.get(id=id)
    oneanswer.likenum+=1
    oneanswer.save()
    res = {"success": "true"}
    return JsonResponse(res)

#登陆错误
def login_view(request):
    if request.method == 'GET':
        return render(request,"login.html")
    elif request.method == 'POST':
        tempuser = request.POST['username']
        temppws = request.POST['password']
        user = authenticate(username=tempuser, password=temppws)
        if user is not None:
            login(request,user)
            return  HttpResponseRedirect("/")
        else:
            return render(request, 'loginError.htmL')

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/login/")

#注册页面
def regina(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        tempuser = request.POST['usernameRegi']
        temppws = request.POST['passRegi']
        tempemail =  request.POST['mailRegi']
        user2=User.objects.filter(username=tempuser)
        if len(user2)!=0:
            return render(request, 'registerError.html')
        else :
            user1=User.objects.create_user(username=tempuser, password=temppws, email=tempemail)
            user1.save()
            user = authenticate(username=tempuser, password=temppws)
            login(request, user)
            return HttpResponseRedirect('/')

