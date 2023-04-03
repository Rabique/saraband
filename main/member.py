from main import *
from flask import Blueprint

blueprint = Blueprint("member", __name__, url_prefix="/member")



@blueprint.route("/join", methods=["GET", "POST"])
def member_join():
    if request.method == "GET":
        return render_template("join.html", title="회원 가입")
    else:
        name = request.form.get("name", type=str)
        email = request.form.get("email", type=str)
        pass1 = request.form.get("pass", type=str)
        pass2 = request.form.get("pass2", type=str)

        if name == "" or email == "" or pass1 == "" or pass2 == "":
            flash("입력되지 않은 값이 있습니다.")
            return render_template("join.html", title="회원 가입")
        
        if pass1 != pass2:
            flash("비밀번호가 일치하지 않습니다.")
            return render_template("join.html", title="회원 가입")
        
        current_utc_time = round(datetime.utcnow().timestamp() * 1000)
        members = mongo.db.members
        post = {
            "name": name,
            "email": email,
            "pass": hash_password(pass1),
            "joindate": current_utc_time,
            "logintime": "",
            "logincount": 0,
        }
        
        x = members.insert_one(post)
        return redirect(url_for("member.member_join"))
           
@blueprint.route("/login", methods=["GET", "POST"])
def member_login():
    if request.method == "GET":
        next_url = request.args.get("next_url", type=str)
        if next_url is not None:
            return render_template("login.html", next_url=next_url, title="회원 로그인")
        else:
            return render_template("login.html", title="회원 로그인")
    else:
        email = request.form.get("email")
        password = request.form.get("pass")
        next_url = request.form.get("next_url")
        
        members = mongo.db.members
        data = members.find_one({"email": email})

        if data is None:
            flash("회원정보가 없습니다.")
            return redirect(url_for("member.member_join"))
        else:
            if check_password(data.get("pass"), password):
            #if data.get("pass") == check_password(password):
                current_utc_time = round(datetime.utcnow().timestamp() * 1000)
                members.update_one({"email": email}, {
                    "$set": {"logintime": current_utc_time},
                    "$inc": {"logincount": 1}
                })
                
                session["email"] = email
                session["name"] = data.get("name")
                session["id"] = str(data.get("_id"))
                session.permanent = True
                if next_url is not None:
                    return redirect(next_url)
                else:
                    return redirect(url_for("board.lists"))
            else:
                flash("비밀번호가 일치하지 않습니다.")
                return redirect(url_for("member.member_login"))
            
            
            

@blueprint.route("/logout")
def member_logout():
    try:
        del session["name"]
        del session["id"]
        del session["email"]
    except:
        pass
    
    return redirect(url_for("member.member_login"))