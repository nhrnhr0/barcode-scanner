import convertapi
import secrects

convertapi.api_secret = secrects.api_secret
convertapi.convert('png', {
    'Url': 'http://3.136.112.72:8010/product/676525117969/'
}, from_format = 'web').save_files('images/')