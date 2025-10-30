from flask import Flask, render_template
import requests

app = Flask(__name__, template_folder="news_archive_templates", static_folder="news_archive_templates")

NEWS_API_URL = "https://api.thenewsapi.com/v1/news/top"

