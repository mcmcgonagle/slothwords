from flask import Flask, request, render_template, session, redirect, url_for
from turbo_flask import Turbo
import game

template_dir = './templates'
app = Flask(__name__, template_folder=template_dir)
turbo = Turbo(app)

app.secret_key = '5#y2LF4Q8zxec'




def start_game():
    session["my_game"] = game.start_game()
    session["guesses"] = []
    session["tiles"] = ['     ', '     ', '     ', '     ','     ', '     ']
    return session["my_game"]

#home page
@app.route('/',methods=['GET','POST'])
def index():
    print(session)
    try:
        if session['my_game'] == None:
            start_game()
    except:
        start_game()
    print(session)
    green_letters = []
    yellow_letters = []
    if request.method == 'POST':
        guess = request.form['guess']
        answer = game.check_guess(guess, session['my_game'], len(session["guesses"]))
        print("guess: ", guess)
        print("answer: ", answer)
        for index, value in enumerate(guess):
            print(index, value)
            try:
                if answer[0][index][0] in guess:
                    green_letters.append(answer[0][index][0])
                else:
                    green_letters.append(" ")

            except:
                green_letters.append(" ")

            try:
                print('here')
                print(answer[0][index][1])
                print(answer[0][index][0])
                if index == answer[1][index][1] and value == answer[1][index][0]:
                    yellow_letters.append(answer[1][index][0])
                else:
                    yellow_letters.append(" ") 
            except:
                yellow_letters.append(" ")


        print("yellow")
        print(yellow_letters)
        print("green")
        print(green_letters)
        if answer == 'win':
            return turbo.stream([
                turbo.append(
                    render_template('_win.html'), target='guesses'),        
            ])
        elif answer == 'lose':
              return turbo.stream([
                turbo.append(
                    render_template('_lose.html'), target='guesses'),        
            ])          
        session["guesses"].append(guess)
        session["tiles"].pop((len(session["tiles"])-1))
        session.modified = True
        if turbo.can_stream():
            return turbo.stream([
                turbo.append(
                    render_template('_guesses.html', guess=guess,green_letters=green_letters,yellow_letters=yellow_letters), target='guesses'),
                turbo.update(
                    render_template('_guess_input.html'), target='form'),
                turbo.update(
                    render_template('_tiles.html', tiles=session["tiles"]), target='tiles')
            ])
        green_letters.clear() 
        yellow_letters.clear()
    return render_template('index.html', guesses=session["guesses"],green_letters=green_letters,yellow_letters=yellow_letters,tiles=session["tiles"])

@app.route('/reset', methods=['GET'])
def reset():
    session["my_game"] = None
    session["guesses"] = []
    session["tiles"] = ['     ', '     ', '     ', '     ','     ', '     ']
    return redirect(url_for('index'))