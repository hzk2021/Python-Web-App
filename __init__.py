from flask import Flask, render_template, request, redirect, url_for, session
import Forms
import win32api, string, random, shelve, Entry, User, Supplier, Reward, Product, Order, Feedback
from datetime import datetime, date, time

# Features/Tasks by Zhenkai: Account Management, Temperature Entry System(with charts for analysis), Reward System, Integrator
# Features/Tasks by Hongray: Supplier list, Order products from supplier
# Features/Tasks by Limchang: Create/add product to shop store, add product to cart
# Features/Tasks by Arief: Customer support (feedback)

app = Flask(__name__, template_folder="templates")

isLoggedIn = False

#region ZHENKAI'S PART
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404

@app.errorhandler(401)
def unauthorised_access(e):
    return render_template('error401.html'), 401

@app.errorhandler(500)
def unauthorised_access(e):
    return render_template('error500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def login():  # to be edited according to active session
    create_login_form = Forms.CreateLoginForm(request.form)

    global isLoggedIn
    wrongCredentials = False

    if isLoggedIn == False:
        if request.method == 'POST' and create_login_form.validate():
            accounts_dict = {}
            db = shelve.open('zkDB.db', 'c')

            try:
                accounts_dict = db['Accounts']
            except:
                print("Error in retrieving Accounts from zkDB.db")

            username = create_login_form.username.data
            password = create_login_form.password.data

            accounts_username_list = []
            for key in accounts_dict:
                accounts_username_list.append(key)

            if username in accounts_username_list:
                if password == accounts_dict[username].get_password():
                    session['logged_in'] = True
                    session['logged_in_user'] = username
                    isLoggedIn = session['logged_in']
                    db.close()
                    return render_template('home_customer.html')
                else:
                    wrongCredentials = True
            else:
                wrongCredentials = True

            db.close()
    else:
        return render_template('home_customer.html')
    return render_template('login.html', form=create_login_form, errorValidate=wrongCredentials)


@app.route('/staffLogin', methods=['GET', 'POST'])
def staff_login():  # to be edited according to active session
    create_login_form = Forms.CreateLoginForm(request.form)

    wrongCredentials = False

    if request.method == 'POST' and create_login_form.validate():
        staffUser = "admin"
        staffPW = "adminPW"

        username = create_login_form.username.data
        password = create_login_form.password.data

        if username == staffUser:
            if password == staffPW:
                return render_template('home_staff.html')
            else:
                wrongCredentials = True
        else:
            wrongCredentials = True
    return render_template('login_staff.html', form=create_login_form, errorValidate=wrongCredentials)


@app.route('/register', methods=['GET', 'POST'])
def register():
    create_register_form = Forms.CreateRegisterForm(request.form)
    global isLoggedIn
    if isLoggedIn == False:
        if request.method == 'POST' and create_register_form.validate():
            accounts_dict = {}
            db = shelve.open('zkDB.db', 'c')

            try:
                accounts_dict = db['Accounts']
            except:
                print("Error in retrieving Accounts from zkDB.db")

            username = create_register_form.username.data
            password = create_register_form.password.data
            email = create_register_form.email.data
            phone_number = create_register_form.phone_number.data

            accounts_username_list = []
            for key in accounts_dict:
                accounts_username_list.append(key)

            if username in accounts_username_list:
                db.close()
                return render_template('/register.html', form=create_register_form, isExist=True, existUser=username)
            else:
                account = User.Customer(username, password, email, phone_number, 20)
                accounts_dict[username] = account
                db['Accounts'] = accounts_dict
                db.close()
                return redirect(url_for('login'))
    else:
        return render_template('home_customer.html')

    return render_template('/register.html', form=create_register_form)


@app.route('/editProfile/<string:username>/', methods=['GET', 'POST'])
def edit_profile(username):
    edit_profile_form = Forms.CreateUpdateForm(request.form)

    global isLoggedIn
    if isLoggedIn == True:
        if request.method == 'POST' and edit_profile_form.validate():
            db = shelve.open('zkDB.db', 'w')
            accounts_dict = db['Accounts']

            account = dict.get(accounts_dict, username)
            account.set_password(edit_profile_form.password.data)
            account.set_phone_number(edit_profile_form.phone_number.data)

            db['Accounts'] = accounts_dict
            db.close()

            return redirect(url_for('home_customer'))
        else:
            db = shelve.open('zkDB.db', 'r')
            accounts_dict = db['Accounts']
            db.close()

            account = dict.get(accounts_dict, username)
            edit_profile_form.username.data = account.get_username()
            edit_profile_form.password.data = account.get_password()
            edit_profile_form.email.data = account.get_email()
            edit_profile_form.phone_number.data = account.get_phone_number()
            edit_profile_form.points.data = account.get_points()
    else:
        return redirect(url_for('login'))

    return render_template('edit_profile.html', form=edit_profile_form)


@app.route('/logout')
def log_out():
    global isLoggedIn
    isLoggedIn = False
    session['logged_in'] = False
    session.pop('logged_in_user', None)
    return redirect(url_for('login'))


@app.route('/customerView')
def home_customer():
    global isLoggedIn
    if isLoggedIn:
        return render_template("home_customer.html")

    return redirect(url_for('login'))



@app.route('/staffView')
def home_staff():
    return render_template("home_staff.html")


@app.route('/createEntry', methods=['GET', 'POST'])
def create_entry():
    create_entry_form = Forms.CreateEntryForm(request.form)
    if request.method == 'POST' and create_entry_form.validate():
        entries_dict = {}
        db = shelve.open('zkDB.db', 'c')

        try:
            entries_dict = db['Entries']
        except:
            print("Error in retrieving Entries from zkDB.db")

        fullName = create_entry_form.full_name.data
        nric = create_entry_form.nric.data
        phone_no = create_entry_form.phone_number.data
        temperature = create_entry_form.temperature.data

        currentDate = date(day=date.today().day, month=date.today().month, year=date.today().year).strftime(
            '%A %d %B %Y')
        currentTime = datetime.strptime(datetime.now().strftime("%H:%M"), "%H:%M").strftime("%I:%M %p")

        entries_id_list = []
        for key in entries_dict:
            entries_id_list.append(key)

        entry_id = 0
        if len(entries_dict) == 0:
            entry_id = 1
        else:
            entry_id = entries_id_list[-1] + 1

        entry = Entry.Entry(entry_id, fullName, nric, phone_no, temperature, currentDate, currentTime, "Click to exit")
        entries_dict[entry_id] = entry
        db['Entries'] = entries_dict

        db.close()

        return redirect(url_for('show_entries'))
    return render_template('/temperature_system/createEntry.html', form=create_entry_form)


@app.route('/showEntries')
def show_entries():
    entries_dict = {}
    entries_list = []
    try:
        with shelve.open('zkDB.db', 'r') as db:
            entries_dict = db['Entries']

        for key in entries_dict:
            entry = entries_dict.get(key)
            entries_list.append(entry)
    except:
        print("Error in retrieving Entries from zkDB.db")
    finally:
        return render_template('/temperature_system/showEntries.html', count=len(entries_list),
                               entries_list=entries_list)


@app.route('/showPieChart')
def show_pie_chart():
    values = []
    times = []

    abnormalCount = 0
    normalCount = 0

    entries_dict = {}

    try:
        with shelve.open('zkDB.db', 'r') as db:
            entries_dict = db['Entries']

        for key in entries_dict:
            entry = entries_dict.get(key)
            values.append(entry.get_temperature())

            rawDateTime = "{} {}".format(entry.get_date().split(None, 1)[1], entry.get_entry_time())
            splitDateTime = datetime.strptime(rawDateTime, "%d %B %Y  %H:%M %p")

            times.append(time(splitDateTime.hour, splitDateTime.minute, splitDateTime.second))

            if entry.get_temperature() > 37.5 or entry.get_temperature() < 35:
                abnormalCount += 1
            else:
                normalCount += 1
    except:
        print("Error in retrieving Entries from zkDB.db")

    return render_template('/temperature_system/pieChart.html', title='Normal vs Abnormal', max=1000, labels=times, values=values, abnormal_count=abnormalCount, normal_count=normalCount, total_count=normalCount+abnormalCount)

@app.route('/showLineChart')
def show_line_chart():
    values = []
    times = []

    entries_dict = {}

    try:
        with shelve.open('zkDB.db', 'r') as db:
            entries_dict = db['Entries']

        for key in entries_dict:
            entry = entries_dict.get(key)
            values.append(entry.get_temperature())

            rawDateTime = "{} {}".format(entry.get_date().split(None, 1)[1], entry.get_entry_time())
            splitDateTime = datetime.strptime(rawDateTime, "%d %B %Y  %H:%M %p")

            times.append(time(splitDateTime.hour, splitDateTime.minute, splitDateTime.second))
    except:
        print("Error in retrieving Entries from zkDB.db")

    return render_template('/temperature_system/lineChart.html', title='Entries', max=45, labels=times, values=values)

@app.route('/showBarChart')
def show_bar_chart():
    entries_dict = {}

    labels = [
        'Monday', 'Tuesday', 'Wednesday', 'Thursday',
        'Friday', 'Saturday', 'Sunday'
    ]

    dayCounts = {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0}
    values = []

    try:
        with shelve.open('zkDB.db', 'r') as db:
            entries_dict = db['Entries']

        for key in entries_dict:
            entry = entries_dict.get(key)

            date = entry.get_date()
            if "Monday" in date:
                dayCounts["Monday"] += 1
            elif "Tuesday" in date:
                dayCounts["Tuesday"] += 1
            elif "Tuesday" in date:
                dayCounts["Wednesday"] += 1
            elif "Tuesday" in date:
                dayCounts["Thursday"] += 1
            elif "Tuesday" in date:
                dayCounts["Friday"] += 1
            elif "Tuesday" in date:
                dayCounts["Saturday"] += 1
            elif "Tuesday" in date:
                dayCounts["Sunday"] += 1

        for key, value in dayCounts.items():
            values.append(value)

        print(values)


    except:
        print("Error in retrieving Entries from zkDB.db")

    return render_template('/temperature_system/barChart.html', title='Daily Customer Count', max=50, values=values, labels=labels)

@app.route('/updateEntry/<int:id>/', methods=['GET', 'POST'])
def update_entry(id):
    update_entry_form = Forms.CreateEntryForm(request.form)
    if request.method == 'POST' and update_entry_form.validate():
        db = shelve.open('zkDB.db', 'w')
        entries_dict = db['Entries']

        entry = dict.get(entries_dict, id)
        entry.set_full_name(update_entry_form.full_name.data)
        entry.set_nric(update_entry_form.nric.data)
        entry.set_phone_no(update_entry_form.phone_number.data)
        entry.set_temperature(float(update_entry_form.temperature.data))

        db['Entries'] = entries_dict
        db.close()

        return redirect(url_for('show_entries'))
    else:
        db = shelve.open('zkDB.db', 'r')
        entries_dict = db['Entries']
        db.close()

        entry = dict.get(entries_dict, id)
        update_entry_form.full_name.data = entry.get_full_name()
        update_entry_form.nric.data = entry.get_nric()
        update_entry_form.phone_number.data = entry.get_phone_no()
        update_entry_form.temperature.data = entry.get_temperature()

        return render_template('/temperature_system/updateEntry.html', form=update_entry_form)


@app.route('/updateExitTime/<int:id>/', methods=['GET', 'POST'])
def update_exit_time(id):
    entries_dict = {}
    db = shelve.open('zkDB.db', 'w')

    try:
        entries_dict = db['Entries']
    except:
        print("Error in retrieving Entries from zkDB.db")

    currentDate = date(day=date.today().day, month=date.today().month, year=date.today().year).strftime('%A %d %B %Y')
    currentTime = datetime.strptime(datetime.now().strftime("%H:%M"), "%H:%M").strftime("%I:%M %p")

    if currentDate != entries_dict[id].get_date():
        entries_dict[id].set_exit_time("11:59 PM")
    else:
        entries_dict[id].set_exit_time(currentTime)

    db['Entries'] = entries_dict

    db.close()

    return redirect(url_for('show_entries'))


@app.route('/deleteEntry/<int:id>/', methods=['POST'])
def delete_entry(id):
    with shelve.open('zkDB.db', 'w') as db:
        entries_dict = db['Entries']
        entries_dict.pop(id)

        db['Entries'] = entries_dict

    return redirect(url_for('show_entries'))

@app.route('/createReward', methods=['GET', 'POST'])
def create_reward():
    create_reward_form = Forms.CreateRewardForm(request.form)
    if request.method == 'POST' and create_reward_form.validate():
        rewards_dict = {}
        db = shelve.open('zkDB.db', 'c')

        try:
            rewards_dict = db['Rewards']
        except:
            print("Error in retrieving Entries from zkDB.db")

        reward_name = create_reward_form.reward_name.data
        points = create_reward_form.points.data

        rewards_id_list = []
        for key in rewards_dict:
            rewards_id_list.append(key)

        reward_id = 0
        if len(rewards_dict) == 0:
            reward_id = 1
        else:
            reward_id = rewards_id_list[-1] + 1

        reward = Reward.Reward(reward_id, reward_name, points)
        rewards_dict[reward_id] = reward
        db['Rewards'] = rewards_dict

        db.close()

        return redirect(url_for('show_rewards'))
    return render_template('/rewards/createReward.html', form=create_reward_form)

@app.route('/showRewards')
def show_rewards():
    rewards_dict = {}
    rewards_list = []
    try:
        with shelve.open('zkDB.db', 'r') as db:
            rewards_dict = db['Rewards']

        for key in rewards_dict:
            reward = rewards_dict.get(key)
            rewards_list.append(reward)
    except:
        print("Error in retrieving Rewards from zkDB.db")
    finally:
        return render_template('/rewards/showRewards.html', count=len(rewards_list),
                               rewards_list=rewards_list)

@app.route('/updateReward/<int:id>/', methods=['GET', 'POST'])
def update_reward(id):
    update_reward_form = Forms.CreateRewardForm(request.form)
    if request.method == 'POST' and update_reward_form.validate():
        db = shelve.open('zkDB.db', 'w')
        rewards_dict = db['Rewards']

        entry = dict.get(rewards_dict, id)
        entry.set_name(update_reward_form.reward_name.data)
        entry.set_points(float(update_reward_form.points.data))

        db['Rewards'] = rewards_dict
        db.close()

        return redirect(url_for('show_rewards'))
    else:
        db = shelve.open('zkDB.db', 'r')
        rewards_dict = db['Rewards']
        db.close()

        entry = dict.get(rewards_dict, id)
        update_reward_form.reward_name.data = entry.get_name()
        update_reward_form.points.data = entry.get_points()

        return render_template('/rewards/updateReward.html', form=update_reward_form)


@app.route('/deleteReward/<int:id>/', methods=['POST'])
def delete_reward(id):
    with shelve.open('zkDB.db', 'w') as db:
        rewards_dict = db['Rewards']
        rewards_dict.pop(id)

        db['Rewards'] = rewards_dict

    return redirect(url_for('show_rewards'))

@app.route('/showUserRewards')
def show_user_rewards():
    rewards_dict = {}
    rewards_list = []
    try:
        with shelve.open('zkDB.db', 'r') as db:
            accounts_dict = db['Accounts']
            rewards_dict = db['Rewards']

        account = dict.get(accounts_dict, str(session['logged_in_user']))
        account_point = account.get_points()

        for key in rewards_dict:
            reward = rewards_dict.get(key)
            if float(account_point) >= float(reward.get_points()):
                rewards_list.append(reward)

    except:
        print("Error in retrieving Rewards from zkDB.db")
    else:
        return render_template('/rewards/showUserRewards.html', count=len(rewards_list),
                               rewards_list=rewards_list, account_point=account_point)

    return render_template('/rewards/noReward.html', count=len(rewards_list),
                           rewards_list=rewards_list)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@app.route('/claimReward/<string:reward_name>/<float:points>', methods=['POST'])
def claim_reward(reward_name, points):
    with shelve.open('zkDB.db', 'w') as db:
        accounts_dict = db['Accounts']
        rewards_dict = db['Rewards']
        account = dict.get(accounts_dict, str(session['logged_in_user']))
        account.deduct_points(float(points))

        db['Accounts'] = accounts_dict
        win32api.MessageBox(0, 'PLEASE THIS COPY DOWN! (' + id_generator(12) + ')', 'Code Number', 0x00001000)

    return redirect(url_for('show_user_rewards'))

#endregion

# region HONGRAY'S PART
@app.route('/addSupplier', methods=['GET', 'POST'])
def add_supplier():
    create_supplier_form = Forms.CreateSupplierForm(request.form)
    if request.method == 'POST' and create_supplier_form.validate():
        suppliers_dict = {}
        db = shelve.open('hongrayDB.db', 'c')

        try:
            suppliers_dict = db['Suppliers']
        except:
            print("Error in retrieving Suppliers from hongrayDB.db.")

        supplier = Supplier.Supplier(create_supplier_form.name.data, create_supplier_form.contact_number.data,
                                     create_supplier_form.email.data, create_supplier_form.address.data,
                                     create_supplier_form.description.data)
        suppliers_dict[supplier.get_supplier_id()] = supplier
        db['Suppliers'] = suppliers_dict

        db.close()

        return redirect(url_for('supplier_list'))
    return render_template('suppliers/addSupplier.html', form=create_supplier_form)


@app.route('/listSupplier')
def supplier_list():
    supplier_dict = {}
    try:
        db = shelve.open('hongrayDB.db', 'c')
        supplier_dict = db['Suppliers']
        db.close()
    except:
        print('Error opening in db')

    supplier_list = []
    for key in supplier_dict:
        supplier = supplier_dict.get(key)
        supplier_list.append(supplier)

    return render_template('suppliers/listSupplier.html', count=len(supplier_list), supplier_list=supplier_list)


@app.route('/updateSupplier/<int:id>/', methods=['GET', 'POST'])
def update_supplier(id):
    update_user_form = Forms.CreateSupplierForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        supplier_dict = {}
        db = shelve.open('hongrayDB.db', 'w')
        supplier_dict = db['Suppliers']

        supplier = supplier_dict.get(id)
        supplier.set_name(update_user_form.name.data)
        supplier.set_contact_number(update_user_form.contact_number.data)
        supplier.set_email(update_user_form.email.data)
        supplier.set_address(update_user_form.address.data)
        supplier.set_description(update_user_form.description.data)

        db['Suppliers'] = supplier_dict
        db.close()

        return redirect(url_for('supplier_list'))
    else:
        supplier_dict = {}
        db = shelve.open('hongrayDB.db', 'r')
        supplier_dict = db['Suppliers']
        db.close()

        supplier = supplier_dict.get(id)
        update_user_form.name.data = supplier.get_name()
        update_user_form.contact_number.data = supplier.get_contact_number()
        update_user_form.email.data = supplier.get_email()
        update_user_form.address.data = supplier.get_address()
        update_user_form.description.data = supplier.get_description()

        return render_template('suppliers/updateSupplier.html', form=update_user_form)


@app.route('/deleteSupplier/<int:id>', methods=['POST'])
def delete_supplier(id):
    supplier_dict = {}
    db = shelve.open('hongrayDB.db', 'w')
    supplier_dict = db['Suppliers']

    supplier_dict.pop(id)

    db['Suppliers'] = supplier_dict
    db.close()

    return redirect(url_for('supplier_list'))


@app.route('/createOrder', methods=['GET', 'POST'])
def create_order():
    supplier_dict = {}
    supplier_list = []
    product_dict = {}
    product_list = []

    try:
        db = shelve.open('hongrayDB.db', 'r')
        supplier_dict = db['Suppliers']
    except:
        print("error in retrieving orders from hongrayDB.db")

    else:
        for supplier_key in supplier_dict:
            supplier_list.append(supplier_dict[supplier_key].get_name())
    try:
        db = shelve.open('limchangDB.db', 'r')
        product_dict = db['Products']
    except:
        print("error in retrieving orders from limchangDB.db")
    else:
        for product_key in product_dict:
            product_list.append(product_dict[product_key].get_name())

    create_order_form = Forms.CreateOrderForm(request.form)
    create_order_form.name.choices = supplier_list
    create_order_form.item.choices = product_list

    if request.method == 'POST' and create_order_form.validate():
        orders_dict = {}

        try:
            db = shelve.open('hongrayDB.db', 'c')
            orders_dict = db['Orders']
        except:
            print("Error in retrieving Orders from hongrayDB.db.")

        order = Order.Order(create_order_form.name.data, create_order_form.item.data,
                            create_order_form.quantity.data)
        orders_dict[order.get_order_id()] = order
        db['Orders'] = orders_dict

        db.close()
        create_order_form.name.choices = supplier_list
        create_order_form.item.choices = product_list
        return redirect(url_for('order_list'))

    return render_template('order_processing/createOrder.html', form=create_order_form)


@app.route('/listOrder')
def order_list():
    orders_dict = {}
    try:
        db = shelve.open('hongrayDB.db', 'r')
        orders_dict = db['Orders']
    except:
        print("error")
    else:
        db.close()

    orders_list = []
    for key in orders_dict:
        order = orders_dict.get(key)
        orders_list.append(order)

    return render_template('order_processing/listOrder.html', count=len(orders_list), orders_list=orders_list)


@app.route('/updateOrder/<int:id>/', methods=['GET', 'POST'])
def update_order(id):
    supplier_dict = {}
    supplier_name = []
    product_dict = {}
    product_name = []
    try:
        db = shelve.open('hongrayDB.db', 'r')
        supplier_dict = db['Suppliers']

    except:
        print("error in retrieving orders from hongrayDB.db")
    else:
        supplier_name.append(supplier_dict[id].get_name())

    try:
        db = shelve.open('limchangDB.db', 'r')
        product_dict = db['Products']
    except:
        print("error in retrieving orders from limchangDB.db")
    else:
        product_name.append(product_dict[id].get_name())

    update_order_form = Forms.CreateOrderForm(request.form)
    update_order_form.name.choices = supplier_name
    update_order_form.item.choices = product_name
    if request.method == 'POST' and update_order_form.validate():
        orders_dict = {}
        db = shelve.open('hongrayDB.db', 'w')
        orders_dict = db['Orders']

        order = orders_dict.get(id)
        order.set_name(update_order_form.name.data)
        order.set_item(update_order_form.item.data)
        order.set_quantity(update_order_form.quantity.data)

        db['Orders'] = orders_dict
        db.close()

        return redirect(url_for('order_list'))
    else:
        orders_dict = {}
        db = shelve.open('hongrayDB.db', 'r')
        orders_dict = db['Orders']
        db.close()

        order = orders_dict.get(id)
        update_order_form.name.data = order.get_name()
        update_order_form.item.data = order.get_item()
        update_order_form.quantity.data = order.get_quantity()

        return render_template('order_processing/updateOrder.html', form=update_order_form)


@app.route('/deleteOrder/<int:id>', methods=['POST'])
def delete_order(id):
    orders_dict = {}
    db = shelve.open('hongrayDB.db', 'w')
    orders_dict = db['Orders']

    orders_dict.pop(id)

    db['Orders'] = orders_dict
    db.close()

    return redirect(url_for('order_list'))


# endregion

#region LIMCHANG'S PART
app.secret_key="secret"

try:
    db = shelve.open('limchangDB.db', 'c')
    orders = db['Orders']
except:
    print("error")
else:
    orders.clear()
    db['Orders'] = orders

db.close()

@app.route('/custshop')
def Customer_shop():
    return render_template("inventory_management/customershop.html")

@app.route('/123')
def view3():
    return render_template("view.html")

@app.route('/view')
def view1():
    return render_template("inventory_management/view.html")

@app.route('/viewstaff')
def view2():
    return render_template("inventory_management/viewstaff.html")

@app.route('/createproduct', methods=['GET', 'POST'])
def create_product():
    create_product = Forms.CreateProduct(request.form)
    if request.method == 'POST' and create_product.validate():
        products_dict = {}
        db = shelve.open('limchangDB.db', 'c')

        try:
            products_dict = db['Products']
        except:
            print("Error in retrieving products from storage.db.")

        products = Product.Product(create_product.Image.data, create_product.Productname.data,
                         create_product.Productstock.data,create_product.Productprice.data, create_product.Description.data)
        products_dict[products.get_product_id()] = products
        db['Products'] = products_dict

        db.close()

        return redirect(url_for('retrieve_product'))
    return render_template('inventory_management/createproduct.html', form=create_product)

@app.route('/viewproduct')
def retrieve_productc():
    products_dict={}
    try:
        db =shelve.open('limchangDB.db','r')
        products_dict = db['Products']
    except:
        print("error limchangDB")
    else:
        db.close()

    products_list = []
    for key in products_dict:
        products = products_dict.get(key)
        products_list.append(products)
    return render_template('inventory_management/customershop.html',count=len(products_list), products_list=products_list)

@app.route('/retrieveproduct')
def retrieve_product():
    products_dict={}
    try:
        db =shelve.open('limchangDB.db','r')
        products_dict = db['Products']
    except:
        print("error")
    else:
        db.close()

    products_list = []
    for key in products_dict:
        products = products_dict.get(key)
        products_list.append(products)
    return render_template('inventory_management/retrieveproduct.html',count=len(products_list), products_list=products_list)

@app.route('/updateProduct/<int:id>/', methods=['GET', 'POST'])
def update_Product(id):
    update_product = Forms.CreateProduct(request.form)
    if request.method == 'POST' and update_product.validate():
        products_dict = {}
        db = shelve.open('limchangDB.db', 'w')
        products_dict = db['Products']

        products = products_dict.get(id)
        products.set_image(update_product.Image.data)
        products.set_name(update_product.Productname.data)
        products.set_stock(update_product.Productstock.data)
        products.set_price(update_product.Productprice.data)
        products.set_specs(update_product.Description.data)


        db['Products'] = products_dict
        db.close()

        return redirect(url_for('retrieve_product'))
    else:
        products_dict = {}
        try:
            db = shelve.open('limchangDB.db', 'r')
        except:
            print("error")
        else:
            products_dict = db['Products']
            db.close()

        products= products_dict.get(id)
        update_product.Image.data = products.get_image()
        update_product.Productname.data = products.get_name()
        update_product.Productstock.data = products.get_stock()
        update_product.Productprice.data=products.get_price()
        update_product.Description.data = products.get_specs()


        return render_template('inventory_management/updatestock.html',form=update_product)
@app.route('/removeitem/<int:id>', methods=['POST'])
def remove_cart_item(id):
    db = shelve.open('limchangDB.db', 'w')
    session.pop('order_number')
    db['itemOrders'].clear()
    db.close()
    return redirect(url_for('itemcart'))

@app.route('/deleteproduct/<int:id>', methods=['POST'])
def delete_product(id):
    products_dict = {}
    db = shelve.open('limchangDB.db', 'w')
    products_dict = db['Products']

    products_dict.pop(id)

    db['Products'] = products_dict
    db.close()

    return redirect(url_for('retrieve_product'))

@app.route('/cart')
def itemcart():
    orders = {}
    db = shelve.open('limchangDB.db', 'r')
    try:
        orders = db['itemOrders']
    except:
        print('Error in retrieving storage.db')

    item_list = []
    if 'order_number' in session:
        item_list = orders[session['order_number']]

    return render_template('inventory_management/addtocart.html', item_list=item_list)

@app.route('/add/<int:id>',methods=['GET', 'POST'])
def additem(id):
    orders ={}

    db = shelve.open('limchangDB.db', 'r')
    items = db['Products']
    db.close()
    db = shelve.open('limchangDB.db','c')
    try:
        orders = db['itemOrders']
    except:
        print('Error in retrieving storage.db')

    if 'order_number' in session:
        order_number= session['order_number']
    else:
        order_number=len(orders)+1
        session['order_number']=order_number
    item2=items.get(id)

    if order_number in orders:
        orders[order_number].append(item2)
    else:
            orders[order_number]=[]
            orders[order_number].append(item2)
    db['itemOrders']=orders
    db.close()
    return redirect(url_for('itemcart'))
@app.route('/payment')
def payment():
    return render_template('inventory_management/payment.html')

#endregion

#region ARIEF'S PART

@app.route('/retrievefeedback')
def retrievefeedback():
    return render_template("customer_support/retrievefeedback.html")

@app.route('/viewF')
def view():
    return render_template("customer_support/view.html")

@app.route('/createfeedback', methods=['GET', 'POST'])
def create_feedback():
    create_feedback = Forms.Createfeedback(request.form)
    if request.method == 'POST' and create_feedback.validate():
        feedbacks_dict = {}
        db = shelve.open('ariefDB.db', 'c')

        try:
            feedbacks_dict = db['Feedback']
        except:
            print("Error in retrieving feedbacks from ariefDB.db.")

        feedbacks = Feedback.Feedback(create_feedback.name.data, create_feedback.phone.data,
                                      create_feedback.email.data, create_feedback.enquiry.data,
                                      create_feedback.service.data, create_feedback.status.data)
        feedbacks_dict[feedbacks.get_feedback_id()] = feedbacks
        db['Feedback'] = feedbacks_dict

        db.close()

        return redirect(url_for('view_feedback'))
    return render_template('customer_support/createfeedback.html', form=create_feedback)

@app.route('/retrieve_feedback')
def retrieve_feedback():
    feedbacks_dict = {}

    try:
        db = shelve.open('ariefDB.db', 'r')
    except:
        print("ariefDB error")
    else:
        feedbacks_dict = db['Feedback']
        db.close()

    feedbacks_list = []
    for key in feedbacks_dict:
        feedbacks = feedbacks_dict.get(key)
        feedbacks_list.append(feedbacks)
    return render_template('customer_support/retrievefeedback.html', count=len(feedbacks_list),
                           feedbacks_list=feedbacks_list)

@app.route('/viewfeedback')
def view_feedback():
    feedbacks_dict = {}

    try:
        db = shelve.open('ariefDB.db', 'r')
    except:
        print("ariefDB error")
    else:
        feedbacks_dict = db['Feedback']
        db.close()

    feedbacks_list = []
    for key in feedbacks_dict:
        feedbacks = feedbacks_dict.get(key)
        feedbacks_list.append(feedbacks)
    return render_template('customer_support/viewcust.html', count=len(feedbacks_list), feedbacks_list=feedbacks_list)

@app.route('/updatefeedback/<int:id>/', methods=['GET', 'POST'])
def update_Feedback(id):
    update_feedback = Forms.Updatefeedback(request.form)
    feedbacks_dict = {}
    db = shelve.open('ariefDB.db', 'r')
    feedbacks_dict = db['Feedback']
    db.close()
    if request.method == 'POST' and update_feedback.validate():
        feedbacks_dict = {}
        db = shelve.open('ariefDB.db', 'w')
        feedbacks_dict = db['Feedback']

        feedbacks = feedbacks_dict.get(id)
        feedbacks.set_name(update_feedback.name.data)
        feedbacks.set_phone(update_feedback.phone.data)
        feedbacks.set_email(update_feedback.email.data)
        feedbacks.set_enquiry(update_feedback.enquiry.data)
        feedbacks.set_service(update_feedback.service.data)
        feedbacks.set_status(update_feedback.status.data)
        db['Feedback'] = feedbacks_dict
        db.close()

        return redirect(url_for('retrieve_feedback'))
    else:
        feedbacks_dict = {}
        db = shelve.open('ariefDB.db', 'r')
        feedbacks_dict = db['Feedback']
        db.close()
        feedbacks = feedbacks_dict.get(id)
        update_feedback.name.data = feedbacks.get_name()
        update_feedback.phone.data = feedbacks.get_phone()
        update_feedback.email.data = feedbacks.get_email()
        update_feedback.enquiry.data = feedbacks.get_enquiry()
        update_feedback.service.data = feedbacks.get_service()
        update_feedback.status.data = feedbacks.get_status()

        return render_template('customer_support/updatefeedback.html', form=update_feedback,
                               service=feedbacks.get_service(), status=feedbacks.get_status())


@app.route('/delete_feedback/<int:id>', methods=['POST'])
def delete_feedback(id):
    feedbacks_dict = {}
    db = shelve.open('ariefDB.db', 'w')
    feedbacks_dict = db['Feedback']

    feedbacks_dict.pop(id)

    db['Feedback'] = feedbacks_dict
    db.close()

    return redirect(url_for('retrieve_feedback'))

#endregion

if __name__ == '__main__':
    app.secret_key = 'ATRiX_key'
    app.run()
