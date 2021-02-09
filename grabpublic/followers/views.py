from django.shortcuts import render
from profiles.models import UserProfile
from .models import Freefollower
from random import sample
from django.utils import timezone
# Create your views here.

def free_10_followers(request):
    if request.method == 'POST':
        print('hellp')
        # pk_range = UserProfile.objects.count()
        #check you followers the user so remove them:
        all_profiles = UserProfile.objects.all()
        user_followers = request.user.is_following.all()
        pk_range = 0
        for profile in all_profiles:
            if not profile in user_followers:
                pk_range +=1
        print(pk_range,'you oouo haud ')
        print(pk_range,'hellp')
        if pk_range >= 10:
            print(pk_range,'hellsp')
            k1, k2, k3, k4, k5, k6, k7, k8, k9, k10 = sample(range(pk_range), 10)
            print(k1,'i am k one')
            # k1, k2 ,k3 = sample(range(pk_range), 3)
            follow_donate=[]
            for profile in all_profiles:
                if not profile in user_followers:
                    follow_donate.append(profile)
            f1 = follow_donate[k1]
            f2 = follow_donate[k2]
            f3 = follow_donate[k3]
            f4 = follow_donate[k4]
            f5 = follow_donate[k5]
            f6 = follow_donate[k6]
            f7 = follow_donate[k7]
            f8 = follow_donate[k8]
            f9 = follow_donate[k9]
            f10 = follow_donate[k10]
            userprofile = request.user.userprofile
            user= request.user
            p = Freefollower.objects.filter(owner=userprofile).exists()
            if p:
                get_p = Freefollower.objects.get(owner=userprofile)
                if not get_p.free_10_followers:
                    p, created = Freefollower.objects.get_or_create(
                        owner=request.user.userprofile,
                        free_10_followers=True,
                        create_date = timezone.now(),)
                    print(created,'hey i know you')
            elif not p :
                user.is_following.add(f1, f2, f3, f4, f5, f6, f7, f8, f9, f10)
                user.save()
           
            
    return render(request,'followers/freefollowers.html',)



def free_10_followers_test(request):
    if request.method == 'POST':
        print('hellp')
        # pk_range = UserProfile.objects.count()
        #check you followers the user so remove them:
        
        for i in range(1,7):
            all_profiles = UserProfile.objects.all()
            user_followers = request.user.is_following.all()
            follow_donate=[]
            pk_range = 0
            for profile in all_profiles:
                if not profile in user_followers:
                    pk_range +=1
            if pk_range >= 10:
                k1, k2 = sample(range(pk_range), 2)
                print(k1,'i am k one')
                for profile in all_profiles:
                    if not profile in user_followers:
                        follow_donate.append(profile)
                f1 = follow_donate[k1]
                f2 = follow_donate[k2]
                userprofile = request.user.userprofile
                user= request.user
                p = Freefollower.objects.filter(owner=userprofile).exists()
                if p:
                    get_p = Freefollower.objects.get(owner=userprofile)
                    if not get_p.free_10_followers:
                        p, created = Freefollower.objects.get_or_create(
                            owner=request.user.userprofile,
                            free_10_followers=True,
                            create_date = timezone.now(),)
                        print(created,'hey i know you')
                elif not p :
                    user.is_following.add(f1,f2)
                    user.save()
           
            
    return render(request,'followers/freefollowers.html',)

