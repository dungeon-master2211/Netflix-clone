from flask import Flask,request,render_template,redirect,flash
import requests
app= Flask(__name__)
API_KEY='c46167285ac0337cc0371b9bb5f040a2'
trending_url='https://api.themoviedb.org/3/trending/all/week?api_key='+API_KEY
action_url='https://api.themoviedb.org/3/discover/movie?api_key=c46167285ac0337cc0371b9bb5f040a2&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_genres=28'
comedy_url='https://api.themoviedb.org/3/discover/movie?api_key=c46167285ac0337cc0371b9bb5f040a2&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_genres=35'
sci_url='https://api.themoviedb.org/3/discover/movie?api_key=c46167285ac0337cc0371b9bb5f040a2&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_genres=878'
family_url='https://api.themoviedb.org/3/discover/movie?api_key=c46167285ac0337cc0371b9bb5f040a2&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_genres=10751'
trending=requests.get(trending_url)
trending_shows=trending.json()
action=requests.get(action_url)
action_shows=action.json()
comedy_shows=requests.get(comedy_url).json()
sci_shows=requests.get(sci_url).json()
family_shows=requests.get(family_url).json()
all_show=trending_shows['results']
action_all=action_shows['results']       
comedy_all=comedy_shows['results']
sci_all=sci_shows['results']
family_all=family_shows['results']
@app.route('/',methods=['GET','POST'])
@app.route('/<string:id>',methods=['GET'])
def index(id='505'):
    hero=trending_shows['results'][0]
    him=hero['backdrop_path']
    ilink='https://image.tmdb.org/t/p/w500'+him
    if hero['media_type']=='tv':
        hname=hero['original_name']
    else:
        hname= hero['original_title']
    '''     
    tlink='https://api.themoviedb.org/3/movie/'+id+'/videos?api_key='+API_KEY+'&language=en-US'
    t=requests.get(tlink).json()
    tr=t['results'][0] '''
    
    return render_template('index.html',hero=hero,ilink=ilink,hname=hname,all_show=all_show,action_all=action_all,comedy_all=comedy_all,sci_all=sci_all,family_all=family_all)

@app.route('/trailer/<string:id>',methods=['GET'])
def trail(id):
    vlink='https://api.themoviedb.org/3/movie/'+id+'/videos?api_key='+API_KEY+'&language=en-US'
    t=requests.get(vlink).json()
    mv='https://api.themoviedb.org/3/movie/'+id+'?api_key='+API_KEY+'&language=en-US'
    mvs=requests.get(mv).json()
    tv='https://api.themoviedb.org/3/tv/'+id+'?api_key='+API_KEY+'&language=en-US'
    tvs=requests.get(tv).json()
    if len(t['results']):
        show=mvs
        stype='movie'
        tlink='https://api.themoviedb.org/3/movie/'+id+'/videos?api_key='+API_KEY+'&language=en-US'
    else:
        show=tvs
        stype='tv'
        tlink='https://api.themoviedb.org/3/tv/'+id+'/videos?api_key='+API_KEY+'&language=en-US'
    t=requests.get(tlink).json()
    tr=t['results'][0]    
    return render_template('trailer.html',tr=tr,show=show,stype=stype)

@app.route('/search',methods=['GET','POST'])
def search():
    if request.method=='POST':
        mv_name=request.form['movie-search']
        li=list(mv_name.split(' '))
        st='%20'.join(li)    
        slink='https://api.themoviedb.org/3/search/movie?api_key='+API_KEY+'&language=en-US&query='+st+'&page=1&include_adult=false'
        sr=requests.get(slink).json()
        return render_template('search.html',sr=sr)

if __name__ =='__main__':
    app.run()