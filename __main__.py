import api.unzipper
def test() :
    api.unzipper.rmtmp()
    unziper = api.unzipper.Unzipper()
    unziper.u_zip("../keyword-generator-master/sous-titres.7z")
    unziper.categorise_all_sub(path_to_move='./data/processed')
    
if __name__ == '__main__':
    # test()
    exit (0)