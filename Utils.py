import datetime
import yaml

class Dates():
    # Grab the cuurent date and return the Year as `2018` and the month as `09`
    # print("Current year: ", datetime.date.today().strftime("%Y"))
    # print("Current Month: ", datetime.date.today().strftime("%m"))
    # year = datetime.date.today().strftime("%Y")
    # month = datetime.date.today().strftime("%m")

    def get_dayDecimal():
        return datetime.date.today().strftime("%d")

    def get_monthDecimal():
        return datetime.date.today().strftime("%m")

    def get_yearDecimal():
        return datetime.date.today().strftime("%Y")


class Configs():
    @staticmethod
    def get_options():
        with open("docs/config.txt", 'r') as ymlfile:
            # rh == remote host name or ip address
            # ru == remote user name
            # rd == remote directory full path should be used
            # rf == remote file if you want to move only one file
            # ld == local directory, full path should be used
            # md == The media files to copy i.e. the directory to copy the files from.
            cfg = yaml.load(ymlfile)
            rh = cfg['remote']['host']
            ru = cfg['remote']['user']
            rd = cfg['remote']['directory']
            rf = cfg['remote']['file']
            ld = cfg['local']['directory']
            sw = cfg['options']['switch']
            md = cfg['remote']['Media']

            return{'optrh':rh, 'optru':ru, 'optrd':rd, 'optrf':rf, 'optld':ld,'optsw':sw, 'optmd':md}