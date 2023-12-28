import pytest
import project


access_token = project.get_access_token()

def test_get_artist():
    #try valid artist
    assert project.get_artist("Willow",access_token) == "3rWZHrfrsPBxVy692yAIxF"
    #try gibberish search
    assert project.get_artist("shshhshs",access_token ) == ""



def test_get_artists_albums():
    #try normal artist
    assert project.get_artists_albums(access_token,"3rWZHrfrsPBxVy692yAIxF" ) == {'<COPINGMECHANISM>': '0oMXn0MNLNyvB4iJPZXOuV', 'lately I feel EVERYTHING': '1dg0gmrCaEbENVXpPIvi1m', 'THE ANXIETY': '2kZyqn4Cmr78D74K9TcO4K', 'WILLOW': '4B2pV5Zds6478QOqA8yqdj', 'The 1st': '0YrdQQiUYjNmLPs0SI53qy', 'ARDIPITHECUS': '0oFPwpDPEsrIYoeGZLFQUv'}
    #try artist with zero albums expected to return empty dict
    assert project.get_artists_albums(access_token,"3pau9bvYGSbZqjCmY1UK8y") == {}
    #try invalid artist id
    assert project.get_artists_albums(access_token,"5mZLaYqN0ZkjxfeUUmiuq" ) == {}
    

def test_albums_tracks():
    # normal request
    assert project.get_album_tracks(access_token,"0oMXn0MNLNyvB4iJPZXOuV") == ['5qMq8ITRVuTwqd2pDL0gff', '0LCHO5qNN5fEncfAIcjtAH', '2OdRGWLkvSccWOrYFlbIFF', '1WCPaQ7zMEMwWbpuTrhM9S', '7fH0VGK95wUN25QN5lmP4c', '2A4pnMV0s7tE00CPiImhLO', '1v3d3KsoHgmiWEI6vFyJ0t', '4OvlUfaJKuZ9aJVAJWmwyE', '0FqkI0vR3Z28v6GSudbKXj', '6ddFCqaAgHeoGaNkaLJ0At', '5w1cL1HG1xJWeBhcUIc1Jw']
    # mac demarcos long album will return only first 40 tracks
    assert project.get_album_tracks(access_token,"70hX7IYqmUGV97OXs2v848" ) == ['5ftED3IYts5K7gChGOUuHG', '5DQnFVwslZtmU0hDgf3wor', '4Qoyylq2zm3eBpENMQ59Xu', '1t6JzKUfGZjoYDZIzkYqSm', '4JwtnmvP4TPi1C1CRwJgiI', '04E2ASMFE8dt2guBV8i0Bd', '6tD7ltNWepcIn7sGAq0wwv', '6MSK4PQrBTaM3j51TrzLM0', '6hMO5tPpQoa2rmOQBhmlx1', '4tX3cJZoR3alDFrdZMOGtV', '4hVsTyDdaliuwc00bYrtsf', '34FNLYnBXyBExIO340XLqx', '46ZE35M0hnO1CeGrXPx1Nu', '3wlFGJ5SJV4o0yYx4o4OlV', '19p6twffpQSqYLBF8MPij6', '6SLCuCK5QExoqqhKexAWuB', '4MCID4Fy8zpZzCRJWiSqXB', '1kBFQhNypLgTw9ouqmIxOO', '4F8zPyKsPM5DTsk2uqqQ8p', '419VY1AgmoxegGhyOhPCuH', '3N8hso233NNlPYJwdSUXNo', '2dSves9EaHZHT9s8eOCcK3', '2ql2ZhziOm1dW2uGI8DLq7', '6unIOeUaYgBZ8TgCWNGDPX', '6L3kq3nfseC0GL1NRPGJaC', '4NDKUI4vFOccDpVTpKRv64', '0khZxbRqdcSPU1GiIgQzkI', '0xCMl9Oymkg8amUwZokFRo', '0fg1xiFdr3DFBYwUzDe5mZ', '5EaxMO1IVSlxo6MV3qKhVV', '3s5HsxVX6spY0ycibLJx2q', '3Vde5vALhDIebbDGGeC5ai', '1BD42GcRTk4kHqdElk8jbx', '7F4HlP13JC2lz2o3xenkpU', '0j4fiXOAYaQNdLb9hDfu8b', '3oUn55qKRZ1JFzfQNbJjS1', '72pFsXc9gE7XKUR9KaN1Ji', '7BxRB28QvwQIsRJpB35Eu2', '3wvW8GIpS8Y95nCt2Wjt5t', '1x7joV0bl6uPwnO3jpfqeb']
    # albums with less than 5 tracks will return empty string
    assert project.get_album_tracks(access_token,"0Hs3BomCdwIWRhgT57x22T" ) == []
    #what happens when invalid id inserted
    assert project.get_album_tracks(access_token,"0Hs3BomCdwIWRhgT57x22" ) == []

def test_tracks_likeability():
    #try couple of tracks
    assert project.tracks_likeability(access_token, ['5qMq8ITRVuTwqd2pDL0gff', '0LCHO5qNN5fEncfAIcjtAH', '2OdRGWLkvSccWOrYFlbIFF', '1WCPaQ7zMEMwWbpuTrhM9S', '7fH0VGK95wUN25QN5lmP4c', '2A4pnMV0s7tE00CPiImhLO', '1v3d3KsoHgmiWEI6vFyJ0t', '4OvlUfaJKuZ9aJVAJWmwyE', '0FqkI0vR3Z28v6GSudbKXj', '6ddFCqaAgHeoGaNkaLJ0At', '5w1cL1HG1xJWeBhcUIc1Jw'] ) == 90.42857142857143
    assert project.tracks_likeability(access_token,['7lIr3vVhpDkU5mQEDcnA0S', '0IW0qaeyxL5Et4UG2MrJKB', '7wL7Lb8Q3aYyq6gmRL0PZq', '5SkRLpaGtvYPhw02vZhQQ9', '6MgGapP3EPFm9kYUvYBTZR', '1ko2NuvWlQdxtNRc8QQzmT', '5g1vtHqi9uV7xtYeCcFOBx', '34j4OxJxKznBs88cjSL2j9', '5b2FFKC64kxqcfaFnIZxoM', '2a1JSfTePKhysdIif2bzut', '1Vp4St7JcXaUoJcIahtf3L', '3A4cpTBPaIQdtPFb5JxtaX', '4KFY4EEv9CN6ivrzD6vEvg', '25mwJPzWVmS2yronBNQJF1', '1th3G3okofWlvGWAAR7Y4V', '5MAY7XyW322jMwLDtBQgsZ', '4BhwlQ9mTwhFGXpQvP9JTV', '62wtttQzoIA9HnNmGVd9Yq', '4mmkhcEm1Ljy1U9nwtsxUo', '5DBmXF7QO43Cuy9yqva116', '7iOhWWYjhhQiXzF4o4HhXN'] ) == 171.14285714285714
    #try to insert invalid track
    assert project.tracks_likeability(access_token, ['5qMq8ITRVuTwqd2pDL0gf', '0LCHO5qNN5fEncfAIcjtAH', '2OdRGWLkvSccWOrYFlbIFF', '1WCPaQ7zMEMwWbpuTrhM9S', '7fH0VGK95wUN25QN5lmP4c', '2A4pnMV0s7tE00CPiImhLO', '1v3d3KsoHgmiWEI6vFyJ0t', '4OvlUfaJKuZ9aJVAJWmwyE', '0FqkI0vR3Z28v6GSudbKXj', '6ddFCqaAgHeoGaNkaLJ0At', '5w1cL1HG1xJWeBhcUIc1Jw']) == 83.28571428571429






