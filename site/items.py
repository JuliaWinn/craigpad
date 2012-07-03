from flask import Blueprint, request, render_template
from wtforms import Form
from wtforms.fields import BooleanField, FormField
import database_utils, math

@app.