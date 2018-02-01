from django.db import models

# Create your models here.

#问题库
class Question(models.Model):
    questionname = models.TextField(max_length=100) #问题名
    content = models.TextField(max_length=300)  #问题描述
    questioner = models.CharField(max_length=100) #提问者username
    answernum = models.IntegerField()   #回答数
    remind = models.IntegerField()

#答案库
class Answer(models.Model):
    content = models.TextField(max_length=300)  #答案内容
    questionid =  models.CharField(max_length=100)  #问题id
    answername = models.CharField(max_length=100)   #回答者username
    likenum = models.IntegerField() #点赞数

#关注库
class Follow(models.Model):
    questionid =  models.CharField(max_length=100)  #问题id
    userid =  models.CharField(max_length=100)  #关注者username

#点赞库
class Like(models.Model):
    answerid = models.CharField(max_length=100) #答案id
    userid = models.CharField(max_length=100)  #用户username

