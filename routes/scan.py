from flask import Blueprint, render_template

scan_bp = Blueprint("scan", __name__)

@scan_bp.route("/")
@scan_bp.route("/url-scan")
def url_scan():
    return render_template("url_scan.html")

@scan_bp.route("/image-scan")
def image_scan():
    return render_template("image_scan.html")

@scan_bp.route("/pdf-scan")
def pdf_scan():
    return render_template("pdf_scan.html")

@scan_bp.route("/text-scan")
def text_scan():
    return render_template("text_scan.html")
