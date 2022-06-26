from flask import Flask, render_template, request, session, Markup
from models import *
app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('homepage.html')

#To-do : Login and Logout Capability

@app.route('/dashboard', methods=["POST"])
def dashboard():
    u_name = request.form.get("username")
    u_pass = request.form.get("password")
    u_list = userList.query.filter_by(userName=u_name).first() # we will store this in The DB
    session['userName'] = u_name
    session['userId'] = u_list.userID
    session['uType'] = u_list.userType
    if u_list.password==u_pass:
        return render_template("dashboard.html")
    else:
        return render_template('homepage.html')  


@app.route('/saveSubject' , methods=["POST"])
def saveSubject():
    sName = request.form.get("subName")
    newSub = Subjects(subName=sName) # not implemented yet
    db.session.add(newSub)
    db.session.commit()
    text=sName+" added Successfully!"
    return render_template("dashboard.html", text=text)


@app.route('/addSubject')
def addSubject():
    subList = Subjects.query.all()
    tabl = '''<div class="form-group">
            <table class="table table-bordered border-success" ><TR style="text-weight:bold; background-color:#ccffcc;">
            <TD>Subject ID</TD>
            <TD>Subject Name</TD></TR>'''
    for item in subList:
        tabl=tabl+"<TR><TD>"+str(item.subId)+"</TD><TD>"+str(item.subName)+"</TD></TR>"

    tabl=tabl+"</table></div>"
    strg='''<h5 style="text-align:center">Add a Subject</h5><HR>
    <form action="/saveSubject" method="post">
    <div class="row mb-3">
    <label for="subName" class="col-sm-2 col-form-label">Subject Name</label>
    <div class="col-sm-10">
      <input type="text" class="form-control" name="subName">
    </div>
  </div>
<div class="col-12">
    <button type="submit" class="btn  btn-success mb-3">Save Subject</button>
</div>

</FORM>
'''+tabl
    text= Markup(strg)
    return render_template("dashboard.html", text=text)

@app.route('/saveBook', methods=["POST"])
def saveBook():
    accNo = request.form.get("accNumber")
    bName = request.form.get("bookName")
    sId = int(request.form.get("subId"))
    authName = request.form.get("author")
    pubName = request.form.get("publisher")
    pages = int(request.form.get("noOfPages"))
    price = int(request.form.get("price"))
    bookMas = bookMaster(accNumber=accNo,bookTitle=bName,SubId=sId,authorName=authName,Publisher=pubName,pages=pages,price=price,status='A')
    db.session.add(bookMas)
    db.session.commit()
    txt = bName+"book Saved Successfully!!!"
    return render_template("dashboard.html",text=txt)


@app.route("/books")
def books():
    bList = bookMaster.query.all()
    tabl = '''<div div class="col-md-12">
            <table class="table table-bordered border-success" ><TR style="text-weight:bold; background-color:#ccffcc;">
            <TD>Accession Number ID</TD>
            <TD>Book Title</TD>
            <TD>Subject</TD></TR>'''
    for item in bList:
        tabl=tabl+"<TR ><TD>"+item.accNumber+"</TD><TD>"+item.bookTitle+"</TD><TD>"+item.subject.subName+"</TD></TR>"
    tabl=tabl+"</TABLE></DIV>"
    sList= Subjects.query.all()
    dd='''<div class="form-group">
            <select class="form-control" name="subID">'''
    for item in sList:
        dd=dd+"<option value=\""+str(item.subID)+"\">"+item.subName +"</option>"
    dd=dd+  '''</select>
</div>'''  
    strg='''<h5 style="text-align:center">Add a Book</h5><HR>
    <form class="row g-3" action="/saveBook" method="post">
  <div class="col-md-6">
    <label for="accNumber" class="form-label">Accession Number</label>
    <input type="text" class="form-control" Name="accNumber">
  </div>
  <div class="col-md-6">
    <label for="subID" class="form-label">Subject ID</label>
    '''+dd+'''
  </div>
  <div class="col-md-6">
    <label for="bookTitle" class="form-label">Book Title</label>
    <input type="text" class="form-control" Name="bookTitle">
  </div>
  <div class="col-md-6">
    <label for="bookAuthor" class="form-label">Author Name</label>
    <input type="text" class="form-control" Name="bookAuthor">
  </div>
  <div class="col-md-12">
    <label for="PublisherName" class="form-label">Publisher</label>
    <input type="text" class="form-control" Name="PublisherName">
  </div>
  
  <div class="col-md-6">
    <label for="pages" class="form-label">Pages</label>
    <input type="text" class="form-control" Name="pages">
  </div>
  <div class="col-md-6">
    <label for="price" class="form-label">Price</label>
    <input type="text" class="form-control" Name="price">
  </div>

<div class="col-12">
    <button type="submit" class="btn  btn-success mb-3">Save Book</button>
</div>
</FORM>'''+tabl
    
    text=Markup(strg)
    return render_template("dashboard.html", text=text)