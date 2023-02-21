from time import sleep
import datetime
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver

from google.cloud import storage
import os
import subprocess


script_start_time = int(time.time())
print(script_start_time)


def upload_file(image_name):

    # create client object
    cred_path = os.path.join(os.path.dirname(__file__), 'credential.json')
    client = storage.Client.from_service_account_json(cred_path)

    # specify the bucket name
    bucket_name = 'trojan-horse'

    # get the bucket
    bucket = client.get_bucket(bucket_name)

    # create a blob object
    blob = bucket.blob(image_name)

    # upload the image to the bucket
    blob.upload_from_filename(image_name)


sleep(10)

driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', options=webdriver.ChromeOptions())


def start_record(script_start_time):
    start_time = int(time.time())

    start_trim = start_time - script_start_time

    return start_trim


def end_record():
    end_time = int(time.time())

    #Stop recording container
    subprocess.run(['docker', 'stop', 'chrome-video'])

    stop_time = int(time.time())

    end_trim = stop_time - end_time

    # Close the web browser
    driver.quit()
    
    return end_trim



tab_list = ['https://www.python.org/', 'https://www.ionic-x.com/', 'https://marketingxpressllc.com/video/vghCMxozE2cJ']
wait_time_list = [5, 5, 5]

def browswer_run(tab_list, wait_time_list):
    #open up all the browsers
    start_trim = start_record(script_start_time)

    i = 0
    for tab in tab_list:
        driver.get(tab)

        time.sleep(int(wait_time_list[i]))

        i+=1

    return start_trim


#command = "ffmpeg -f lavfi -i color=c=red:s=1920x1080:d=5 -c:v libx264 -r 30 -pix_fmt yuv420p output.mp4"
#subprocess.run(command.split(), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


browswer_start_time = int(time.time())

print(browswer_start_time - script_start_time)

start_trim = browswer_run(tab_list, wait_time_list)

i = 182
# specify the image file name
#image_name = '{0}_{1}.png'.format("hello", i)
# Take a screenshot
#driver.save_screenshot(image_name)
#upload_file(image_name)

end_trim = end_record()
print(end_trim)
print(end_trim)
print(end_trim)

start_trim_cmd = 'ffmpeg -i ./videos/chrome_video.mp4 -ss {0} -c copy ./videos/output1.mp4'.format(start_trim)
subprocess.run(start_trim_cmd.split(), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

time.sleep(5)

#end_trim_cmd = 'ffmpeg -sseof -{0} -i ./videos/output1.mp4 -c copy ./videos/outputf.mp4'.format(end_trim)
#end_trim_cmd ='ffmpeg -i ./videos/output1.mp4 -ss 00:00:00 -t `ffprobe -i ./videos/output1.mp4 -show_entries format=duration -v quiet -of csv="p=0"`-{0} -c:v copy -c:a copy ./videos/outputf.mp4'.format(end_trim)
#subprocess.run(end_trim_cmd.split(), check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

duration_cmd = 'ffprobe -i ./videos/output1.mp4 -show_entries format=duration -v quiet -of csv="p=0"'
duration = subprocess.check_output(duration_cmd, shell=True).strip().decode('utf-8')
duration = float(duration)

trim_duration = duration - end_trim

ffmpeg_cmd = 'ffmpeg -i ./videos/output1.mp4 -ss 00:00:00 -t {0} -c:v copy -c:a copy ./videos/outputf.mp4'.format(trim_duration)
subprocess.run(ffmpeg_cmd, shell=True)

'ffmpeg -i ./videos/output1.mp4 -t `ffprobe -i ./videos/output1.mp4 -show_entries format=duration -v quiet -of csv="p=0"`-{0} -c:v copy -c:a copy ./videos/outputf.mp4'.format(end_trim)

sleep(10)

print("Starting outputf.mp4 upload to Google")
upload_file('./videos/outputf.mp4')

# Shut down Docker Compose
#subprocess.call("docker-compose down", shell=True)


#   Editing in docker container
#   docker-compose.yml on gcloud VM
#   