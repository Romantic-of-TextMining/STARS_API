# Add the targeted files to Google Drive
from google.colab import drive
drive.mount('/content/drive')
mydrive ="/content/drive/My Drive/Text Mining/"
files = ['PublicEngagement_plat.xlsx', 'PublicEngagement_bron.xlsx']

# Read the two excel respectively
df0 = pd.read_excel(mydrive+files[0], header=None).iloc[3:,:7]
df1 = pd.read_excel(mydrive+files[1], header=None).iloc[3:,:7]

#class ServerFileManager:
#    @classmethod
