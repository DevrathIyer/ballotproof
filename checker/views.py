from django.shortcuts import render,redirect
from .forms import AddressForm
import requests
import os
import boto3
import logging
import json
logger = logging.getLogger('testlogger')


boto_kwargs = {
    "aws_access_key_id": os.environ["AWS_ACCESS_KEY_ID"],
    "aws_secret_access_key": os.environ["AWS_SECRET_ACCESS_KEY"],
    "region_name": os.environ["AWS_REGION"],
}
s3_client = boto3.Session(**boto_kwargs).client("s3")


URL = "https://api.geocod.io/v1.6/geocode"
geocodio_key = os.environ['geocodio_key']
# Create your views here.
def home(request):

    if request.method == "POST":
        # do congressional lookup thing
        form = AddressForm(request.POST)
        if form.is_valid():

            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            street = form.cleaned_data['street']
            zip = form.cleaned_data['zip']

            address = street + " " + city + " " + state + " " + str(zip)
            r = requests.get(URL, {"q":address,"fields":"cd","api_key":geocodio_key})

            district = r.json()["results"][0]["fields"]["congressional_districts"][0]["district_number"]

        return redirect('check',state=state,district=district)

    else:
        form = AddressForm()
        return render(request, 'checker/index.html', {"form":form})

def check(request,state="AZ",district=5):

    response = s3_client.list_objects_v2(
            Bucket="congressional-distrct-bucket",
            MaxKeys=100 )


    filename = "{}/{}-{}-2.json".format(state,state,district)
    try:
        raw = s3_client.get_object(Bucket='congressional-distrct-bucket', Key=filename)['Body'].read().decode('utf-8')
    except:
        return render(request,'checker/no_annotation.html',{})

    annotation = json.loads(raw)

    return render(request, 'checker/app.html', {"state":state,"district":district,"annotation":annotation})