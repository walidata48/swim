from argparse import Action
from pydoc import classname
from tkinter.ttk import Style
#from app import app
#from app import server
import flask
import json
from dash import html, dcc, callback, Input, Output, State
import dash_daq as daq
from datetime import datetime
from dash import dash_table
import pandas as pd
from users import users_info
import sqlite3
from flask import Flask, render_template, session
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import dash

app = dash.Dash(
    "Swimming Atlet",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)
server = app.server
app.config.suppress_callback_exceptions = True
app.title = "Swimming Club"
app.description = """A dashboard to display price indicators for Bitcoin, 
                  Ethereum, Ripple, and Bitcoin-cash."""
log_form = html.Div([
    
    html.Form([
        html.Span('Login', className='title'),
        html.Span('Welcome To CSA App', className='subtitle'),
        html.Div([
            dcc.Input(placeholder="username", name="username", type="text", className='input'),
            dcc.Input(placeholder="password", name="password", type="password"  , className='input'),],className='form-container') ,
        dbc.Button("Login", type="submit", )
    ] , action="/login", method="post", className='form'), 
], className='form-box')


reg_form = html.Div([
    html.Form([
        html.Span('Registrasi', className='title'),
        html.Span('Registrasi Atlit', className='subtitle'),
        html.Div([
        dcc.Input(id = 'newname', placeholder="name", name="username", type="text", className='input'),
        dcc.Input(id = 'tgl', placeholder="tanggal lahir", name="username", type="text", className='input'),
        dcc.Input(id = 'newuser', placeholder="username", name="username", type="text", className='input'),
        dcc.Input(id = 'newpass', placeholder="password", name="password", type="password", className='input'),], className='form-container'),
        html.Div(id='zero'),
        dbc.Button("Registrasi", type="submit", id='register')
    ] ,action="/login", method="post",className='form'), 
], className='form-box' )


_app_route = "/"


# Create a login route
@app.server.route("/login", methods=["POST"])
def route_login():
    with sqlite3.connect("datas.db") as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM data')
        row = cur.fetchall()
        user_pwd = dict(row)
    #user_pwd, user_names = users_info()
    data = flask.request.form
    username = data.get("username")
    password = data.get("password")

    if username not in user_pwd.keys() or user_pwd[username] != password:
        return flask.redirect("/login")
    else:

        # Return a redirect with
        rep = flask.redirect(_app_route)

        # Here we just store the given username in a cookie.
        # Actual session cookies should be signed or use a JWT token.
        rep.set_cookie("custom-auth-session", username)
        return rep


# Simple dash component login form.
login_form = html.Div(
    [
        html.Form(
            [
                dcc.Input(placeholder="username", name="username", type="text"),
                dcc.Input(placeholder="password", name="password",
                          type="password"),
                html.Button("Login", type="submit"),
            ],
            action="/login",
            method="post",
        )
    ]
)


form = dbc.Container(
    dbc.Row([
        dbc.Col(
            reg_form, sm=12, md=6, className='card1'),
        dbc.Col(log_form, sm=12, md=6, className='card1')
    ], className='row1')
)



# create a logout route
@app.server.route("/logout", methods=["POST"])
def route_logout():
    # Redirect back to the index and remove the session cookie.
    rep = flask.redirect("/login")
    rep.set_cookie("custom-auth-session", "", expires=0)
    return rep


app.layout = html.Div(
    [
        html.H1('Cilegon Swimmer Club'),
        html.Div(id="custom-auth-frame"),  # Input for buttons
        html.Div(
            
            id="custom-auth-frame-1",  # Output after Login or Logout
            
        ),
        #dcc.Dropdown(['NYC', 'MTL', 'SF'], 'NYC', id='demo-dropdown'),
        html.Div(id="graph-output", ),
        #reg_form,
        html.H2(id='out')
    ],
    
)



@app.callback(
       # Output('out', 'children'),
        Output("custom-auth-frame-1", "children"),
        Output("graph-output", "children"),
        Input("out", "children"), 
)
def render_content(start):
    session_cookie = flask.request.cookies.get("custom-auth-session")

    if not session_cookie:
        # If there's no cookie we need to login.
        return [
            form,
            
            "",
            
        ]
    else:
        logout_output = html.Div(
            children=[
                html.Div(
                    html.H3("Hello {} !".format(session_cookie)),
                    
                ),
                html.Div(
                    dcc.LogoutButton(logout_url="/logout", className='btn btn-primary'),
                                    ),
            ],
            className='header',
        )
        
        name_input = dbc.Row([dbc.Col(dbc.Input(id = 'name', placeholder=f"[{session_cookie}", className='field' ), ), ], className="mb-3",)
        lomba = dbc.Container(dbc.Row([dbc.Col([html.H3('Daftar Lomba', style={'margin-bottom': '15px'}, className='text-center'), dbc.Input(id = 'id_solved', placeholder=f"{session_cookie}", style={'margin-bottom': '15px'}, ), dcc.Dropdown( id='dropdown_parameter', options=['Bebas', 'Kupu-kupu', 'Punggung',], value='pH', style={'margin-bottom': '15px'} ), dbc.Button(id ='submit_solved', children = 'Submit', n_clicks = 0 )], )
                 ,
                 ], className='g-2 mt-5'))
        return logout_output, lomba
    
@app.callback(
       
        Output("zero", "children"),
        Input("register", "n_clicks"),
        State('newname', 'value'),
        State('tgl', 'value'),
        State('newuser', 'value'),
        State('newpass', 'value'),
        
        prevent_initial_call=True 
)
def render_content(start, names, tgl, newuser, newpass):
    #global user_pwd
    with sqlite3.connect("datas.db") as con:
          
      cur = con.cursor()
      cur.execute("insert into newuser (name, tgl, username, password) values (?,?,?,?)", (names, tgl, newuser, newpass))
      con.commit()

    with sqlite3.connect("datas.db") as con: 
      cur = con.cursor() 
      cur.execute("insert into data (name, password) values (?,?)", (newuser, newpass))
      con.commit()

    
   
         
   
    return " "   

@app.callback(
       
        Output("id_solved", "value"),
        Input("submit_solved", "n_clicks"),
        State('dropdown_parameter', 'value'),
        
        prevent_initial_call=True 
)
def render_content(start,lomba):
    name = flask.request.cookies.get("custom-auth-session")


    with sqlite3.connect("datas.db") as con:
           
      cur = con.cursor()
      cur.execute("insert into regist (name, lomba) values (?,?)", (name, lomba))
      con.commit()
      
    return "1"





if __name__ == "__main__":
    app.run_server(debug=False, )



