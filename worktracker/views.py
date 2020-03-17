from django.shortcuts import render
import datetime
from datetime import timedelta
from django.contrib.auth.models import User
from worktracker.models import Login_data,Task,Userstat,Lunch,Break,Rules
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import HttpResponse
import json
from django.core import serializers
from django.http import JsonResponse
from django.utils import timezone
from .forms import View_3_form,Stop_task_form,Rules_form
import pprint
import random
from django.contrib import messages
from celery.schedules import crontab
from celery.task import periodic_task
# Create your views here.

@periodic_task(run_every=crontab(hour=23, minute=40,))
def every__morning():
    now = datetime.datetime.now(datetime.timezone.utc)
    print("This is run every night at 11:40")
    print("for every user if there are any login objects , or break objects without out time  . then set out time as this ")
    l = Lunch.objects.filter(create_on=datetime.datetime.today()).update(lunch_out=now,notes="auto completed by code")
    print(f"number of lunch items updated {l}")
    b = Break.objects.filter(create_on=datetime.datetime.today()).update(break_out=now)
    print(f"number of break items updated {b}")

@login_required
def worktracker(request):
    context_data = {}
    context_data["title"] = "WorkTracker - home "
    #initially view is 1
    context_data["view_type"] = "1"
    pp = pprint.PrettyPrinter(indent=4)
    now = datetime.datetime.now(datetime.timezone.utc)
    if request.method == 'POST':
        print("Post data")
        pp.pprint(request.POST)

        if request.is_ajax():
            if request.POST.get("sidetrack_trigger"):
                print(Userstat.objects.filter(user=request.user).update(current_side_track="show_sidetrack_list"))
                print("in view giving out side track list")
                return render(request, 'worktracker/side_track.html')

            if request.POST.get("save_rule_trigger"):
                rule, notes = request.POST.get("rule"), request.POST.get(
                    "notes")
                existing_rule = Rules.objects.filter(user=request.user)
                new_rule = Rules(user=request.user,rule=rule,notes=notes,rule_no = len(existing_rule)+1)
                new_rule.save()
                print(Userstat.objects.filter(user=request.user).update(current_side_track="show_sidetrack_list"))
                print(" giving out side track list")
                return render(request, 'worktracker/side_track.html')

            if request.POST.get("rule_trigger"):
                print(Userstat.objects.filter(user=request.user).update(current_side_track="show_rules"))
                print("in view rendering life rules  ")
                rules  = Rules.objects.filter(user=request.user)
                if len(rules)>3:
                    rand_rule = []
                    for _ in range(3):
                        rand_rule.append(random.choice(rules))
                        context_data['rule_list'] = rand_rule
                    print(rand_rule)
                rule_form = Rules_form()
                context_data["rule_form"]=rule_form
                return render(request, 'worktracker/rules.html',context_data)

            if request.POST.get("lunch_data_trigger"):
                print(Userstat.objects.filter(user=request.user).update(current_side_track="get_lunch_data"))
                context_data['side_track'] ="get_lunch_data"
                print("in view givinh out break")
                l = Lunch.objects.filter(user=request.user, create_on=datetime.datetime.today())
                print("lunch data n\n\n\n")
                if len(l) == 0:
                    print("no lunch data ")
                    context_data["not_in_lunch"] = True
                else:
                    print("check if user has gone for lunch ")
                    if l.first().lunch_out:
                        print("user completed lunch ")
                        context_data["lunch_data"] = "went to lunch at " + str(
                            l.first().lunch_in.strftime("%H:%M:%S")) + " \
                            came back at " + str(l.first().lunch_out.strftime("%H:%M:%S"))
                    else:
                        context_data["lunch"] = True
                        context_data["lunch_data"] = "went to lunch at " + str(l.first().lunch_in.strftime("%H:%M:%S"))
                        print("time since lunch == ")
                        delta = now - l.first().lunch_in
                        print(delta.total_seconds())
                        context_data["lunch_time"] = delta.total_seconds()
                ##geting break data
                b = Break.objects.filter(user=request.user,
                                         create_on=datetime.datetime.today(), break_out=None
                                         )
                if (len(b) == 0):
                    print("No breaks are running ")
                else:
                    context_data["break"] = True
                    delta = now - b.first().break_in
                    print(delta.total_seconds())
                    context_data["break_time"] = delta.total_seconds()
                    context_data["break_tittle"] = b.first().break_tittle

                context_data["break_list"] = Break.objects.filter(user=request.user,
                                                                  create_on=datetime.datetime.today()
                                                                  )
                return render(request, 'worktracker/lunch.html',context_data)


            if request.POST.get("current_view") =="2":
                print("in view to redirect to view_2 html ")
                context_data["current_task"] = Task.objects.filter(user=request.user, completed=False)
                return render(request, 'worktracker/view_2.html', context=context_data)
            if request.POST.get("current_view") == "1":
                print("in view changing to viw 1 html ")
                context_data["current_task"] = Task.objects.filter(user=request.user, completed=False)
                return render(request, 'worktracker/view_1.html', context=context_data)

            if request.POST.get("task_info_trigger"):
                print("in info view  calling view 3 ")
                context_data["view_type"] = "3"
                id = request.POST.get("task_id")
                print(id)
                task = Task.objects.filter(pk=int(id)).first()
                print(task)

                print("getting sub task ")
                subtask = Task.objects.filter(isparent=task.pk)
                print(subtask)
                if len(subtask)==0:
                    print("no subtask found ")
                else:
                    context_data["subtask"] = True
                    context_data["subtask_list"]=subtask

                context_data["current_task"] = task
                form_view_3 = View_3_form(instance=task)
                context_data["current_task_form"] = form_view_3
                return render(request, 'worktracker/view_3.html', context=context_data)

            if request.POST.get("task_update_trigger"):
                print("saving model task instance  ")
                id = request.POST.get("task_id")
                print(id)
                task = Task.objects.filter(pk=int(id)).first()
                print(task)
                form_view_3 = View_3_form(request.POST,instance=task)
                if form_view_3.is_valid():
                    form_view_3.save()
                    print("saving the task info from view 3")
                else:
                    print("form not valid ")
                print("saving task changing to viw 1 html ")
                context_data["current_task"] = Task.objects.filter(user=request.user, completed=False)
                return render(request, 'worktracker/view_1.html', context=context_data)

            if request.POST.get("going_for_lunch"):
                print("going to lunch at ",end="")
                print(now)
                l_today = Lunch(user=request.user)
                l_today.save()
                new_run_json = {}
                time_now = datetime.datetime.now()
                current_time = time_now.strftime("%H:%M:%S")
                new_run_json["lunch_data"] = "Going to lunch at "+l_today.lunch_in.strftime("%H:%M:%S") +"..."
                return JsonResponse(new_run_json, status=200)

            if request.POST.get("stopping_lunch"):
                print("stopping lunch at ",end="")
                print(now)
                l_today = Lunch.objects.filter(user=request.user,
                                               create_on=datetime.datetime.today()
                                               ).update(lunch_out=now)
                l = Lunch.objects.get(user=request.user,
                                     create_on=datetime.datetime.today()
                                     )
                new_run_json = {}
                time_now = datetime.datetime.now()
                current_time = time_now.strftime("%H:%M:%S")
                new_run_json["lunch_data"] = "Went to lunch at "+l.lunch_in.strftime("%H:%M:%S") +\
                                             "came back at "+ l.lunch_out.strftime("%H:%M:%S")
                return JsonResponse(new_run_json, status=200)


            if request.POST.get("going_for_break"):
                print("going to break at ",end="")
                print(now)
                break_tittle = request.POST.get("break_tittle")
                b_today = Break(user=request.user,break_tittle=break_tittle)
                b_today.save()
                new_run_json = {}
                print("created a new break "+break_tittle)
                return JsonResponse(new_run_json, status=200)

            if request.POST.get("stopping_break"):
                print("stopping break at ",end="")
                print(now)
                b_today = Break.objects.filter(user=request.user,
                                               create_on=datetime.datetime.today(), break_out=None
                                               ).first()
                comepleted_break = Break.objects.filter(user=request.user,
                                               create_on=datetime.datetime.today(),break_out=None
                                               ).update(break_out=now)
                b_now = Break.objects.get(pk = b_today.pk)
                print(comepleted_break)
                new_run_json = {}
                httpres= '<li class="list-group-item">'+b_now.break_tittle\
                                           +' .... '+b_now.break_in.strftime("%H:%M") +':'\
                                   +b_now.break_out.strftime("%H:%M")+' </li>'
                return HttpResponse(httpres)

            if request.POST.get("task_start_trigger") :
                print("starting new task ")
                task_id  = request.POST.get("task_id")
                new_stat_task = Task.objects.get(pk=int(task_id))
                print("starting this task =")
                print(new_stat_task)
                u = Userstat.objects.filter(user=request.user)
                if len(u) == 0:
                    print("no active data for user se this task as first data")
                    u = Userstat(user=request.user)
                    u.save()
                else:
                    print("already user data is there ")
                    print("getting old running task ")
                    previous_running = u.first().current_task
                    print(previous_running)
                    if previous_running:
                        print("already there is a task ")
                        if u.first().is_running:
                            print("updating old task time spent from html and is running to false ")
                            time_spent = request.POST.get("time_task")
                            print(time_spent)
                            split_days = int(time_spent.split()[0])
                            split_time = time_spent.split()[2].split(":")
                            delta = timedelta(days=split_days,
                                              seconds=int(split_time[2]),

                                              minutes=int(split_time[1]),

                                              hours=int(split_time[0]),
                                              )
                            print("delta time")
                            print(delta)
                            print("old task time spent  = ")
                            Task.objects.filter(pk=previous_running.pk).update(timetaken=delta)
                        else:
                            print("previous task was not running ")
                        Task.objects.filter(pk=previous_running.pk).update(temp_start=None)

                new_start_json = {}
                new_start_json["time_taken"]=0
                print("setting new task as current and not starting it ")
                new_start_user = Userstat.objects.filter(user=request.user).update(current_task=new_stat_task,is_running=False)
                print(new_start_user)
                if new_stat_task.timetaken :
                    print("new task was already running ")
                    new_start_json["time_taken"]= new_stat_task.timetaken.total_seconds()
                else:
                    print("first time running this task ")
                new_start_json["tittle"]= new_stat_task.tittle
                pp.pprint(new_start_json)
                return JsonResponse(new_start_json, status=200)

            if request.POST.get("task_run_trigger"):
                time_spent = request.POST.get("time_task")
                current_user_stat = Userstat.objects.filter(user=request.user).first()
                print("running current task ")
                print(Userstat.objects.filter(user=request.user).update(is_running=True))
                print("updating user stat and current task temp start ")
                new_run_json = {}
                #worst case we have one querry extra . habe this shit completed

                print("time recived ")
                print(time_spent)
                new_run_json["time"] = 0
                delta = timedelta(seconds=0)
                if not (time_spent) == "0" and time_spent.find:
                    print("task was already running ")
                    split_days = int(time_spent.split()[0])
                    split_time = time_spent.split()[2].split(":")
                    delta = timedelta(days=split_days,
                                      seconds=int(split_time[2]),

                                      minutes=int(split_time[1]),

                                      hours=int(split_time[0]),
                                      )
                    print("delta time")
                    print(delta)
                    print("old task time spent  = ", end="")
                else:
                    print("old task not already  running ")
                    delta = timedelta(seconds=0)
                    # user_task = Task.objects.filter(pk=int(current_user_stat.current_task.pk)).update(temp_start=now,timetaken=delta)
                print("total time ",end="")
                print(delta.total_seconds())
                print(Task.objects.filter(pk=int(current_user_stat.current_task.pk)).update(temp_start=now))
                print(Task.objects.filter(pk=int(current_user_stat.current_task.pk)).update(timetaken=delta))
                new_run_json["time"]=delta.total_seconds()
                return JsonResponse(new_run_json, status=200)


            if request.POST.get("task_pause_trigger"):
                print("Pause current task \n")
                time_spent = request.POST.get("current_running_time")
                print("current running time is :",end ="")
                print(time_spent)
                split_days = int(time_spent.split()[0])
                split_time = time_spent.split()[2].split(":")
                delta = timedelta(days=split_days,
                                  seconds=int(split_time[2]),

                                  minutes=int(split_time[1]),

                                  hours=int(split_time[0]),
                                  )
                print("delta time ; ",end="")
                print(delta)
                current_task = Userstat.objects.filter(user=request.user).first()

                print("updating time spent for task and temp time")
                task_change = Task.objects.filter(pk=current_task.current_task.pk).update(timetaken=delta,temp_start=None)
                print(task_change)
                print("currrent stat is set to not running so that we have changes in ui ")
                Userstat.objects.filter(user=request.user).update(is_running=False)
                new_run_json={}
                return JsonResponse(new_run_json, status=200)

            if request.POST.get("task_stop_trigger"):
                print("going to stop current task \n")
                time_spent = request.POST.get("current_stop_time")
                print("current running time is :",end ="")
                print(time_spent)
                split_days = int(time_spent.split()[0])
                split_time = time_spent.split()[2].split(":")
                delta = timedelta(days=split_days,
                                  seconds=int(split_time[2]),

                                  minutes=int(split_time[1]),

                                  hours=int(split_time[0]),
                                  )
                print("delta time ; ",end="")
                print(delta)
                current_task = Userstat.objects.filter(user=request.user).first()

                print("updating time spent for task and temp time")
                task_change = Task.objects.filter(pk=current_task.current_task.pk).update(timetaken=delta,temp_start=None)
                print(task_change)
                print("currrent stat is set to not running so that we have changes in ui ")
                Userstat.objects.filter(user=request.user).update(is_running=False)
                new_run_json={}
                print("checking subtask ")
                print(current_task.current_task.pk)
                subtask_list =  Task.objects.filter(user=request.user,isparent=current_task.current_task.pk)
                print(subtask_list)
                for subtask in subtask_list:
                    print(subtask)
                    if subtask.completed == False:
                        messages.success(request, f'There is a sub task remaining')
                        print("sub task not completed ")
                        print("calling info view ")
                        context_data["view_type"] = "3"
                        task = Task.objects.filter(pk=current_task.current_task.pk).first()
                        print(task)

                        print("getting sub task ")
                        subtask = Task.objects.filter(isparent=task.pk)
                        print(subtask)
                        if len(subtask) == 0:
                            print("no subtask found ")
                        else:
                            context_data["subtask"] = True
                            context_data["subtask_list"] = subtask

                        context_data["current_task"] = task
                        form_view_3 = View_3_form(instance=task)
                        context_data["current_task_form"] = form_view_3
                        return render(request, 'worktracker/view_3.html', context=context_data)

                print("calling the task stop view")
                task = Task.objects.filter(pk=current_task.current_task.pk).first()
                print(task)
                context_data["current_task"] = task
                stop_task = Stop_task_form(instance=task)
                context_data["current_task_form"] = stop_task
                return render(request, 'worktracker/stop_task.html', context=context_data)


            if request.POST.get("task_stop_completely"):
                ending=request.POST.get("ending")
                print("saving model task instance and stopig task completely ")
                current_task = Userstat.objects.filter(user=request.user).first()
                print("stopping task is ",end="")
                print(current_task.current_task)
                Task.objects.filter(pk=current_task.current_task.pk).update(ending=ending, completed=True)

                Userstat.objects.filter(user=request.user).update(is_running=False,current_task=None)
                print("saving the task endng info and closing it ")

                print("saving task changing to viw 1 html ")
                context_data["current_task"] = Task.objects.filter(user=request.user, completed=False)
                return render(request, 'worktracker/view_1.html', context=context_data)


            if request.POST.get("task_not_stop"):
                print("not stoping task  ")
                print("changing to viw 1 html ")
                context_data["current_task"] = Task.objects.filter(user=request.user, completed=False)
                return render(request, 'worktracker/view_1.html', context=context_data)

            if request.POST.get("subtask_create_trigger"):
                print("Creating new subtask ")
                parent_id = request.POST.get("task_id")
                tittle, priority, type = request.POST.get("subtask_tittle"), request.POST.get(
                    "subtask_priority"), request.POST.get("subtask_type")
                new_task = Task(user=request.user, tittle=tittle, priority=int(priority), type=type,isparent=int(parent_id))
                new_task.save()
                print("added new subtask goin gback to info view")
                task = Task.objects.filter(pk=int(parent_id)).first()
                print(task)

                print("getting sub task ")
                subtask = Task.objects.filter(isparent=task.pk)
                print(subtask)
                if len(subtask) == 0:
                    print("no subtask found ")
                else:
                    context_data["subtask"] = True
                    context_data["subtask_list"] = subtask

                context_data["current_task"] = task
                form_view_3 = View_3_form(instance=task)
                context_data["current_task_form"] = form_view_3
                return render(request, 'worktracker/view_3.html', context=context_data)


            if request.POST.get("task_create_trigger"):
                print("Creating new task ")
                tittle, priority, type = request.POST.get("task_tittle"), request.POST.get("task_priority"), request.POST.get("task_type")
                new_task = Task(user=request.user,tittle=tittle,priority=int(priority),type=type)
                new_task.save()
                context_data["current_task"]= Task.objects.filter(user=request.user,completed=False)
                return render(request, 'worktracker/view_1.html', context=context_data)

            if request.POST.get("login_start_trigger"):
                print("log in trigger")
                print("system time is ")
                print(now)
            #create a login instance its called by login_start_trigger
            #ITS FOR A perticular user and only when the start button is enabled
            # mae sure the start button is only enabled for user if he is  not logged in for the day
                login_instance = Login_data(user=request.user,login_time=now)
                login_instance.save()
                return JsonResponse({"login_time": now,"user":request.user.username}, status=200)
            if request.POST.get("logout_trigger"):
                print("log out trigger")
                #login for login start button
                #if user s already logined in then send that loged in

                #get login time and get time spent thne add to logout and close
                login_time  =  Login_data.objects.get(user=request.user,login_date=now).login_time
                hour, min, sec = int(request.POST.get("hour")), int(request.POST.get("minutes")), int(request.POST.get("seconds"))
                time_spent = datetime.timedelta(seconds=(9*60*60 - (hour*60*60+min*60+sec)))
                logout_time_new = login_time + time_spent
                data_changed=Login_data.objects.filter(user=request.user,login_date=now).update(log_out=logout_time_new)
                print("Saved log out data ")
                return JsonResponse({"logout_time": now}, status=200)
                #add a condition that only if user was logged in then add log out data
                #better is if you make th elogout visible only if the user data is there
                #so everyting is on get  . if user is there and not logged in then login else logout
    elif request.method == "GET":
        print("In Get, nothing special just a print :) \n")
    print("Check running task ")
    u = Userstat.objects.filter(user=request.user)
    #this is required because initially user filter returns zero so this condition . this works sanme as other



    if len(u) == 0:
        print("No active data for user ")
        context_data["running_task"] =False
    else:
        #here check for u.task
        context_data['side_track']=u.first().current_side_track
        print("user has current  task ?")
        if u.first().current_task:
            print("user has a task in curent  ")
            pp.pprint(u.first())
            context_data["running_task"] = u.first()
            print("is task running ? ")
            if  u.first().is_running ==True:
                print("Task is runnning . get seconds by adding time spent and last temp start  ")
                context_data["is_running"] = True
                #check if there is an instanc runing for this task which we strted before
            task_time_running = 0
            print("temp ")
            print(u.first().current_task.temp_start)
            if u.first().current_task.temp_start :
                print("Task was already running since ::  ",end="")
                cur = Userstat.objects.filter(user=request.user).first()
                print(cur.current_task.temp_start)
                temp_time = now - cur.current_task.temp_start
                print("time in seconds till now :: ",end = " ")
                print(temp_time.total_seconds())
                task_time_running +=temp_time.total_seconds()
            if u.first().current_task.timetaken:
                print("previous time taken")
                task_time_running += u.first().current_task.timetaken.total_seconds()
            print(task_time_running)
            #since temp_time is zero by default it will not be problem if not running already
            context_data["task_time_running"]=task_time_running
        else:
            print("No running task for user ")
            context_data["running_task"] = False

    ##get lunch data

            #get all post by user and not closed
    print("Geting all curent task ")
    context_data["current_task"] = Task.objects.filter(user=request.user,completed=False)
    context_data["time_spent"] = "32401"


    #login check logic
    user_login_data = Login_data.objects.filter(user=request.user,login_date=now)
    if user_login_data:
        print("User already  logged in. Now checking logout")
        print("Logout time : ",end="")
        first_login = user_login_data.first()
        print(first_login.log_out)
        if first_login.log_out:
            print("User was logged out ")
            context_data["logged_out"]=True
        else:
            #get time spent and add it
            print("Not logged out getting time spent ")
            time_spent = now - first_login.login_time
            context_data["time_spent"]= 32401 - int(str(time_spent.total_seconds()).split(".")[0])
            context_data["logged_in"]=True
    #There are three data sent back
    #so check them in templet
    pp.pprint(context_data)
    return render(request,'worktracker/worktracker.html',context=context_data)


def test(request):
    return render(request,'worktracker/test.html',{'title':'test '})