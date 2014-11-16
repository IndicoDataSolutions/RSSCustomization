from setuptools import setup, find_packages

setup(
    name = "rss_customization",
    version = "0.1",
    author = "Indico Data Solutions",
    author_email = "contact@indico.io",
    description = ("RSS feed customization using the indico text tags API."),
    license = "BSD",
    url = "http://github.com/IndicoDataSolutions/RSSCustomization",
    install_requires = [
        'Flask>=0.10.1',
        'feedparser>=5.1.3',
        'indicoio>=0.4.10' 
    ],
    packages = find_packages()
)