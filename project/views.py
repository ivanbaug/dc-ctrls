import os
from project.models import Device
from project.forms import NewDeviceForm
from flask import(Blueprint,
                  redirect,
                  render_template,
                  request,
                  url_for,
                  flash)
from flask_login import login_required, current_user
from datetime import datetime
from pytz import timezone
from . import db

main = Blueprint('main', __name__)

tz = timezone("America/Lima")
INFO_EMAIL = os.environ.get('INFO_EMAIL')


@main.route('/')
def index():
    return render_template("index.html")


@main.route('/profile')
@login_required
def profile():
    return render_template("profile.html")


@main.route('/man-dev', methods=['GET', 'POST'])
@login_required
def manage_devices():
    devices = Device.query.all()
    # devices = []

    return render_template("managedevices.html", info_email=INFO_EMAIL, devices=devices)


@main.route('/new-dev', methods=['GET', 'POST'])
@login_required
def add_device():
    new_device_form = NewDeviceForm()
    # TODO:handle devices with same name
    if new_device_form.validate_on_submit():

        print('this was a post request')
        new_device = Device(
            name=new_device_form.name.data,
            dev_type=new_device_form.dev_type.data,
            di=new_device_form.di.data,
            ai=new_device_form.ai.data,
            ui=new_device_form.ui.data,
            do=new_device_form.do.data,
            ao=new_device_form.ao.data,
            co=new_device_form.co.data,
            has_clock=new_device_form.has_clock.data,
            price=new_device_form.price.data,
            date_created=datetime.now(tz=tz),
            date_modified=datetime.now(tz=tz),
            user_created=current_user.name,
            user_modified=current_user.name,
        )
        print('generated new device, trying toadd')
        # print('trying to create a new device')
        db.session.add(new_device)
        db.session.commit()
        print('this should be enough, it should have committed')
        return redirect(url_for('main.manage_devices'))
    print('this was a get request')
    return render_template("newdevice.html", info_email=INFO_EMAIL, form=new_device_form)


@main.route('/about')
@login_required
def about():
    return render_template("about.html", info_email=INFO_EMAIL)


@main.route("/delete/<int:device_id>")
@login_required
def delete_device(device_id):
    device_to_delete = Device.query.get(device_id)
    db.session.delete(device_to_delete)
    db.session.commit()
    return redirect(url_for('main.manage_devices'))


# TODO: Implement the following to display the devices

# def listPossibleCtrls(req,ctrl_sol_list,ctrls,exs):
#     #req : requirements
#     #ctrl_sol_list : list of controller solutions
#     #ctrls : general list of available controller objects
#     #exs : general list of available expansion module objects
#     main_list=[]
#     for c in ctrl_sol_list:
#         solution_list=[c.cost]

#         used_io, total_remaining, required = getUsedIO(req,c.io_list)

#         cne_strings = c.name_array #Stands for controllers and expansion string list

#         controller = objectByName(ctrls,cne_strings[0])
#         used, remaining, required = getUsedIO(req,controller.io_list)

#         cdict = createModuleDict(controller.name, used)
#         solution_list.append(cdict)

#         for e in cne_strings[1:]:
#             expansion = objectByName(exs,e)
#             used, remaining, required = getUsedIO(required,expansion.io_list)
#             edict = createModuleDict(expansion.name, used)
#             solution_list.append(edict)
#         rem_dict = createModuleDict("Available", total_remaining)
#         solution_list.append(rem_dict)
#         main_list.append(solution_list)

#     return main_list
