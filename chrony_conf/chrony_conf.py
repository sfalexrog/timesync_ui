
class ChronyConf:
    def __init__(self, configfile='/etc/chrony/chrony.conf'):
        self.configfile = configfile
        self.config = dict()


    def parseConfig(self):
        with open(self.configfile, 'r') as cf:
            for line in cf.readlines():
                sline = line.strip()
                # Ignore comments and empty lines
                if sline.startswith('#') or sline == '':
                    continue
                lineparts = sline.split()
                option = lineparts[0]
                if len(lineparts) > 1:
                    self.config[option] = lineparts[1:]
                else:
                    self.config[option] = ['']


    def writeConfig(self):
        with open(self.configfile, 'w') as cf:
            for option, value in self.config.iteritems():
                optlist = [option]
                optlist.extend(str(val) for val in value)
                optline = ' '.join(optlist)
                cf.write(optline)
                cf.write('\n')


    @staticmethod
    def readConfig(configfile = '/etc/chrony/chrony.conf'):
        conf = ChronyConf(configfile=configfile)
        conf.parseConfig()
        return conf
