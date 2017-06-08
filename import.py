from app import create_app
from importer.data_importer import DataImporter

# instantiate app instance so that we can load mongo configurations
# and use them in the importer implementation
app = create_app()


def run_importer():

    # This is to expand the app's context(scope),
    # so that we can use mongo configurations for the importer too.
    with app.app_context():
      DataImporter().run()

if __name__ == '__main__':
    run_importer()