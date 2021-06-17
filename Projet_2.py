import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px
import altair as alt
import urllib.request
import PIL.Image
from PIL import Image
import requests
from linkpreview import link_preview
import streamlit.components.v1 as components
import time
import plotly.graph_objs as go
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pydeck as pdk
import webbrowser
import base64
import datetime

# Import bases de données
df_bases_acteurs = pd.read_csv(
    "https://github.com/Seb-Dupont-DataAnalyst/Movie-Recommendation-Engine\df_staff.tsv")
df_bases_filmsFR = pd.read_csv(
    "https://github.com/Seb-Dupont-DataAnalyst/Movie-Recommendation-Engine\df_bases_filmsFR_2")

df_bases_visu = pd.read_csv(
    "https://github.com/Seb-Dupont-DataAnalyst/Movie-Recommendation-Engine\df_bases_filmsFR_visu_2")

df_acteurs_visu = pd.read_csv(
    "https://github.com/Seb-Dupont-DataAnalyst/Movie-Recommendation-Engine\df_staff_visu_2")
df_bases_KNN_F = pd.read_csv(
    "https://github.com/Seb-Dupont-DataAnalyst/Movie-Recommendation-Engine\df_bases_KNN_F")
X_bis = pd.read_csv(
    "https://github.com/Seb-Dupont-DataAnalyst/Movie-Recommendation-Engine\X_bis")
voisins_final = pd.read_csv(
    "https://github.com/Seb-Dupont-DataAnalyst/Movie-Recommendation-Engine\voisins_final")

def translate(x):
    translation = {'Comedy': 'Comédie', 'Fantasy': 'Fantastique', 'Romance': "Romance", 'Drama':'Drame', 'War':'Guerre',
                 'Musical': 'Musique', 'Action': 'Action', 'Crime': "Crime", 'Horror':'Horreur', 'Mystery':'Mystère',
                 'Adventure': 'Aventure', 'Thriller': 'Policier', 'Sci-Fi': "Sci-Fi", 'Western':'Western', 'History':'Historique',
                 'Biography': 'Biographie', 'Animation': 'Animation', 'Music': "Musique", 'Family':'Famille', 'Sport':'Sport',
                 'Documentary' : 'Documentaire'}
    for i in translation:
        y=translation.get(x, x)
        return y

def translate_c(x):
    translation = {"UK":"Royaume-Uni", "Spain":"Espagne", "Germany": "Allemagne", "Belgium" : "Belgique", "West Germany":"Allemagne", "WestGermany":"Allemagne", "EastGermany":"Allemagne","Lebanon":"Liban", "Sweden":"Suède",
                  "East Germany":"Allemagne", "Poland":"Pologne", "Brazil":"Brésil", "Denmark":"Danemark","USA":"États-Unis",
                  "Italy":"Italie", "Switzerland":"Suisse", "Yugoslavia":"Yougoslavie", "Taiwan":"Taiwan", "Liechtenstein":"Liechtenstein",
                  "Czechoslovakia":"Tchécoslovaquie", "Russia" : "Russie", "Soviet Union":"Russie", "SovietUnion":"Russie", "Japan":"Japon", "Egypt":"Egypte", "Mexico":"Mexique",
                  "Australia":"Australie", "Greece":"Grèce", "Philippines":"Philippines", "Algeria":"Algerie", "Austria" : "Autriche", "China" : "Chine"}
    for i in translation:
        y=translation.get(x, x)
        return y

# Titre principale
#components.html("<body style='color:white;font-family:verdana; font-size:60px; border: 2px solid white; text-align: center; padding: 1px'><b>Cinéma Le Creusois</b></body>")
st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)
st.markdown('<body class="title">Cinéma Le Creusois</body>', unsafe_allow_html=True)

# Création Sidebar avec les différents choix
st.sidebar.title("Bonjour :movie_camera:")
st.sidebar.write("Que souhaitez vous faire aujourd'hui?")
choice = st.sidebar.selectbox("", ('Accueil', "S'enregistrer", 'Le cinéma en quelques chiffres','Les acteurs dans le cinéma','Le top 10',
                         'Recommandations personnalisées',"Suggestion de films",'Nos soirées spéciales','Nos tarifs' ,'Nous contacter'))

# Paramétrage suivant le choix effectué dans la Sidebar
if choice == 'Accueil':
    st.markdown("""  <style> .reportview-container { background:
    url("https://wallpapercave.com/wp/wp3157716.jpg")}
    </style> """, unsafe_allow_html=True)

    im = Image.open(requests.get(
        "https://www.leshouches.fr/wp-content/uploads/2015/10/cin%C3%A9ma.jpg", stream=True).raw)
    st.image(im, use_column_width=True)

    components.html("<p style='color:white;font-family:verdana; font-size:20px; text-align: left'><i>Bienvenue sur notre tout nouveau site internet, vous pouvez dès à présent parcourir nos différents onglets pour trouver LE FILM qui vous correspond. Notre tout nouvel outil vous guidera vers une sélection personnalisée.</i></p>")

if choice == "S'enregistrer":

 
    
    st.write("")
    st.write("")
    st.write("")
    st.write("")
  
    st.markdown('<body class="p3">Créer votre compte</body>', unsafe_allow_html=True)
    st.write("")
    st.write("")

    col1, col2 = st.beta_columns(2)

    with col1:
        field_1 = st.text_input('Prénom')
        field_3 = st.text_input("Ville")
        field_4 = st.text_input("Email")
    with col2:
        field_2 = st.text_input('Nom')
        start_date = datetime.date(1950, 7, 6)
        date = st.date_input('Date de naissance', start_date)
        field_5 = st.text_input("Film préféré")
    #lets try a both a text input and area as well as a date
    
    st.button('Envoyer')


elif choice == 'Le cinéma en quelques chiffres':
    st.write('')
    st.write('')
    st.markdown("""  <style> .reportview-container { background:
    url("https://wallpaperaccess.com/full/2300291.jpg")}
    </style> """, unsafe_allow_html=True)

    # On paramètre notre slider qui sert à choisir la période que l'on souhaite étudier
    years = []
    for i in range(2020, 1969, -1):
        years.append(i)
    year_to_filter = st.select_slider('Choisissez la période à étudier:',options=years)
    filtered_data = df_bases_filmsFR[df_bases_filmsFR['startYear']
                                     >= year_to_filter]
    filtered_data2 = df_acteurs_visu[(df_acteurs_visu['startYear'] >= year_to_filter)
                                     & ((df_acteurs_visu['category'].str.contains('act')))]

    # Graph 2
    #st.write("Répartition des films par genre:")
    
    def count_genre(x):
        # on concatène à la suite toutes les lignes pour avoir une série qui regroupe tous les genres
        data_plot = filtered_data[x].str.cat(sep=',')
        data = pd.Series(data_plot.split(','))
        # conts each of the genre and return.
        info = data.value_counts(ascending=False)
        # voir pour le nombre
        return info

    count_genre('genres')
    compteur = pd.DataFrame(count_genre('genres'))
    new_compteur = compteur.reset_index()


    new_compteur['index'] = new_compteur['index'].apply(translate)
    
    new_compteur.columns = ['Genres', 'Nb films']

    fig2, ax = plt.subplots(figsize=(15, 10))
    fig2 = px.bar(new_compteur, x=new_compteur['Genres'], y=new_compteur['Nb films'], labels=dict(
        x="Genres", y="Nb Films"), color=new_compteur['Nb films'], height=400, color_continuous_scale=px.colors.sequential.Teal)
    fig2.layout.coloraxis.showscale = False
    fig2.update_layout(title='<b>Nombre de films par genre</b>',
                       title_x=0.5, title_font_family="Verdana")
    fig2.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
                       'paper_bgcolor': 'rgba(0,0,0,0)', })
    st.write(fig2)

    # Graph 3
    
    def count_genrePct(x):
        # on concatène à la suite toutes les lignes pour avoir une série qui regroupe tous les genres
        data_plot = filtered_data[x].str.cat(sep=',')
        data = pd.Series(data_plot.split(','))
        # conts each of the genre and return.
        info = data.value_counts(ascending=False, normalize=True)
        return info

    count_genrePct('genres')
    genre = count_genrePct('genres')
    tresh = 0.027
    b = genre[genre > tresh]
    b['Autres'] = genre[genre <= tresh].sum()
    b = b.reset_index()
    b['index'] = b['index'].apply(translate)


    fig3 = px.pie(b, values=0, names='index', labels='index',
                  color_discrete_sequence=px.colors.sequential.Teal)
    fig3.update_layout(width=800, height=500)
    fig3.update_traces(textposition='inside')
    fig3.update_traces(texttemplate = "%{label} <br>%{percent:%f}")
    fig3.update_layout(title='<b>Répartition des films par genre</b>',
                       title_x=0.5, title_font_family="Verdana")
    fig3.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
                       'paper_bgcolor': 'rgba(0,0,0,0)', })
    st.write(fig3)


    # Graph 5
    
    def count_country(x):
        # on concatène à la suite toutes les lignes pour avoir une série qui regroupe tous les genres
        data_plot = filtered_data[x].str.cat(sep=',')
        data = pd.Series(data_plot.split(','))
        newlist = []
        for i in data:
            j = i.lstrip()
            newlist.append(j)
        dataNew = pd.Series(newlist)
        # conts each of the genre and return.
        info = dataNew.value_counts(ascending=False)
        return info

    countries = count_country('country')
    moyenne = count_country('country').mean()
    
    tresh = moyenne * 2
    e = countries[countries > tresh]
    e['Autres'] = countries[countries <= tresh].sum()
    e = e.reset_index()
    e['index'] = e['index'].apply(translate_c)   

    fig6, ax = plt.subplots(figsize=(15, 10))
    fig6 = px.bar(e, x='index', y=0, labels=dict(
        x="Pays", y="Nb Films"), color=0, height=400, color_continuous_scale=px.colors.sequential.Teal)
    fig6.layout.coloraxis.showscale = False
    fig6.update_layout(title='<b>Nombre de films par pays</b>',
                       title_x=0.5, title_font_family="Verdana", xaxis_title = "Pays", yaxis_title = "Nb Films")
    fig6.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
                       'paper_bgcolor': 'rgba(0,0,0,0)', })
    st.write(fig6)

    
    def count_country_pct(x):
        # on concatène à la suite toutes les lignes pour avoir une série qui regroupe tous les genres
        data_plot = filtered_data[x].str.cat(sep=',')
        data = pd.Series(data_plot.split(','))
        newlist = []
        for i in data:
            j = i.lstrip()
            newlist.append(j)
        dataNew = pd.Series(newlist)
        # conts each of the genre and return.
        info = dataNew.value_counts(ascending=False, normalize=True)
        return info

    country = count_country_pct('country')
    tresh = 0.015
    c = country[country > tresh]
    c['Autres'] = country[country <= tresh].sum()
    c = c.reset_index()
    c['index'] = c['index'].apply(translate_c)

    fig5 = px.pie(c, values=0, names='index', labels='index',
                  color_discrete_sequence=px.colors.sequential.Teal)
    fig5.update_traces(textposition='inside')
    fig5.update_traces(texttemplate = "%{label} <br>%{percent:%f}")
    fig5.update_layout(width=800, height=500)
    fig5.update_layout(title="<b>Répartition des films par pays d'origine</b>",
                       title_x=0.5, title_font_family="Verdana")
    fig5.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
                       'paper_bgcolor': 'rgba(0,0,0,0)', })
    st.write(fig5)

    #New graph
    df_bases_filmsFR_country = df_bases_filmsFR
    df_bases_filmsFR_country['country'] = df_bases_filmsFR_country['country'].str.split(',', n=1, expand=True)
    df_bases_filmsFR_country['country'] = df_bases_filmsFR_country['country'].apply(translate_c)
    liste_pays = df_bases_filmsFR_country['country'].unique().tolist()
    liste_pays.insert(0,'Tous')
    choix_pays = st.selectbox(
    'Choisir le pays', liste_pays)
    
    if choix_pays != 'Tous':

        df_bases_filmsFR_country = df_bases_filmsFR_country[df_bases_filmsFR_country['country'] == choix_pays] 
        df_bases_filmsFR_country = df_bases_filmsFR_country[(df_bases_filmsFR_country['startYear']>= year_to_filter) & (df_bases_filmsFR_country['startYear']<2020)]

        pivot_films1 = pd.DataFrame(df_bases_filmsFR_country.pivot_table(values = ['averageRating', 'runtimeMinutes', 'numVotes'], index = 'startYear', aggfunc = 'mean'))
        pivot_films2 = pd.DataFrame(df_bases_filmsFR_country.pivot_table(values = ['title'], index = 'startYear', aggfunc = 'count'))
        pivot = pivot_films1.merge(pivot_films2, left_on='startYear', right_on='startYear', how='inner')

        fig21 = make_subplots(specs=[[{"secondary_y": True}]])    
        fig21.add_trace(go.Scatter(x=pivot.index, y=pivot["averageRating"], name="Notes"),secondary_y=False)
        fig21.add_trace(go.Scatter(x=pivot.index, y=pivot["title"], name="Nb Films"),secondary_y=True)
        fig21.update_layout(title_text="<b>Evolution des notes et du nombre de films", title_x=0.5, title_font_family="Verdana")
        fig21.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)','paper_bgcolor': 'rgba(0,0,0,0)'})
        fig21.update_xaxes(showgrid=False, gridwidth=1, gridcolor='black')
        fig21.update_yaxes(showgrid=False, gridwidth=1, gridcolor='black')
        fig21.update_xaxes(title_text="Années", dtick=5, linecolor ='rgba(0,0,0,0)')
        fig21.update_yaxes(title_text="<b>Notes", secondary_y=False, dtick = 2, range = [0,10])
        fig21.update_yaxes(title_text="<b>Nb Films", secondary_y=True, rangemode = "tozero")
      
        st.write(fig21)

        fig29 = make_subplots(specs=[[{"secondary_y": True}]])    
        fig29.add_trace(go.Scatter(x=pivot.index, y=pivot["averageRating"], name="Notes"),secondary_y=False)
        fig29.add_trace(go.Scatter(x=pivot.index, y=pivot["numVotes"], name="Nb Votes"),secondary_y=True)
        fig29.update_layout(title_text="<b>Evolution des notes et du nombre de votes", title_x=0.5, title_font_family="Verdana")
        fig29.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)','paper_bgcolor': 'rgba(0,0,0,0)'})
        fig29.update_xaxes(showgrid=False, gridwidth=1, gridcolor='black')
        fig29.update_yaxes(showgrid=False, gridwidth=1, gridcolor='black')
        fig29.update_xaxes(title_text="Années", dtick=5, linecolor ='rgba(0,0,0,0)')
        fig29.update_yaxes(title_text="<b>Notes", secondary_y=False, dtick = 2, range = [0,10])
        fig29.update_yaxes(title_text="<b>Nb votes", secondary_y=True, rangemode = "tozero")
        st.write(fig29)

        fig7 = px.scatter(df_bases_filmsFR_country, x="averageRating", y="runtimeMinutes", trendline="ols")
        fig7.update_layout(title_text="<b>Corrélation entre notes et durée des films", title_x=0.5, title_font_family="Verdana")
        fig7.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)','paper_bgcolor': 'rgba(0,0,0,0)'})
        fig7.update_xaxes(showgrid=False, gridwidth=1, gridcolor='black', linecolor ='rgba(0,0,0,0)')
        fig7.update_yaxes(showgrid=False, gridwidth=1, gridcolor='black', linecolor ='rgba(0,0,0,0)')
        fig7.update_xaxes(title_text="<b>Notes", dtick = 2, range = [0,10])
        fig7.update_yaxes(title_text="<b>Durée", dtick = 50, range = [0,200])
        st.write(fig7)

        col1, col2, col3 = st.beta_columns(3)

        with col1:
            st.write("")
        with col2:
            data_corr2 = df_bases_filmsFR_country.corr()
            data_corr3 = data_corr2.loc['averageRating','runtimeMinutes']
            my_formatter = "{0:.2f}"
            output = my_formatter.format(data_corr3)
            st.write("indice de corrélation :", output)

        with col3:
            st.write("")

        fig4 = px.box(df_bases_filmsFR_country, x="startYear", y="averageRating")
        fig4.update_layout(title_text="<b>Evolution de la répartition des notes", title_x=0.5, title_font_family="Verdana")
        fig4.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)','paper_bgcolor': 'rgba(0,0,0,0)'})
        fig4.update_xaxes(showgrid=False, gridwidth=1, gridcolor='black', linecolor ='rgba(0,0,0,0)')
        fig4.update_yaxes(showgrid=False, gridwidth=1, gridcolor='black')
        fig4.update_yaxes(title_text="<b>Notes", dtick = 2, range = [0,10])
        fig4.update_xaxes(title_text="<b>Années")

        st.write(fig4)

    else:
        #df_bases_filmsFR_country = df_bases_filmsFR_country[df_bases_filmsFR_country['country'] == choix_pays] 
        df_bases_filmsFR_country = df_bases_filmsFR_country[(df_bases_filmsFR_country['startYear']>= year_to_filter) & (df_bases_filmsFR_country['startYear']<2020)]

        pivot_films1 = pd.DataFrame(df_bases_filmsFR_country.pivot_table(values = ['averageRating', 'runtimeMinutes', 'numVotes'], index = 'startYear', aggfunc = 'mean'))
        pivot_films2 = pd.DataFrame(df_bases_filmsFR_country.pivot_table(values = ['title'], index = 'startYear', aggfunc = 'count'))
        pivot = pivot_films1.merge(pivot_films2, left_on='startYear', right_on='startYear', how='inner')

        fig21 = make_subplots(specs=[[{"secondary_y": True}]])    
        fig21.add_trace(go.Scatter(x=pivot.index, y=pivot["averageRating"], name="Notes"),secondary_y=False)
        fig21.add_trace(go.Scatter(x=pivot.index, y=pivot["title"], name="Nb Films"),secondary_y=True)
        fig21.update_layout(title_text="<b>Evolution des notes et du nombre de films", title_x=0.5, title_font_family="Verdana")
        fig21.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)','paper_bgcolor': 'rgba(0,0,0,0)'})
        fig21.update_xaxes(showgrid=False, gridwidth=1, gridcolor='black')
        fig21.update_yaxes(showgrid=False, gridwidth=1, gridcolor='black')
        fig21.update_xaxes(title_text="Années", dtick=5, linecolor = 'rgba(0,0,0,0)')
        fig21.update_yaxes(title_text="<b>Notes", secondary_y=False, dtick = 2, range = [0,10])
        fig21.update_yaxes(title_text="<b>Nb Films", secondary_y=True, rangemode = "tozero")
        st.write(fig21)
        
        fig29 = make_subplots(specs=[[{"secondary_y": True}]])    
        fig29.add_trace(go.Scatter(x=pivot.index, y=pivot["averageRating"], name="Notes"),secondary_y=False)
        fig29.add_trace(go.Scatter(x=pivot.index, y=pivot["numVotes"], name="NB Votes"),secondary_y=True)
        fig29.update_layout(title_text="<b>Evolution des notes et du nombre de votes", title_x=0.5, title_font_family="Verdana")
        fig29.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)','paper_bgcolor': 'rgba(0,0,0,0)'})
        fig29.update_xaxes(showgrid=False, gridwidth=1, gridcolor='black')
        fig29.update_yaxes(showgrid=False, gridwidth=1, gridcolor='black')
        fig29.update_xaxes(title_text="Années", dtick=5, linecolor = 'rgba(0,0,0,0)')
        fig29.update_yaxes(title_text="<b>Notes", secondary_y=False, dtick = 2, range = [0,10])
        fig29.update_yaxes(title_text="<b>Nb votes", secondary_y=True, rangemode = "tozero")
        st.write(fig29)

        fig7 = px.scatter(df_bases_filmsFR_country, x="averageRating", y="runtimeMinutes", trendline="ols")
        fig7.update_layout(title_text="<b>Corrélation entre notes et durée des films", title_x=0.5, title_font_family="Verdana")
        fig7.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)','paper_bgcolor': 'rgba(0,0,0,0)'})
        fig7.update_xaxes(showgrid=False, gridwidth=1, gridcolor='black', linecolor ='rgba(0,0,0,0)')
        fig7.update_yaxes(showgrid=False, gridwidth=1, gridcolor='black', linecolor ='rgba(0,0,0,0)')
        fig7.update_xaxes(title_text="<b>Notes", dtick = 2, range = [0,10])
        fig7.update_yaxes(title_text="<b>Durée", dtick = 50, range = [0,200])
        st.write(fig7)

        col1, col2, col3 = st.beta_columns(3)

        with col1:
            st.write("")
        with col2:
            data_corr2 = df_bases_filmsFR_country.corr()
            data_corr3 = data_corr2.loc['averageRating','numVotes']
            my_formatter = "{0:.2f}"
            output = my_formatter.format(data_corr3)
            st.write("indice de corrélation :", output)

        with col3:
            st.write("")

        fig4 = px.box(df_bases_filmsFR_country, x="startYear", y="averageRating")
        fig4.update_layout(title_text="<b>Evolution de la répartition des notes", title_x=0.5, title_font_family="Verdana")
        fig4.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)','paper_bgcolor': 'rgba(0,0,0,0)'})
        fig4.update_xaxes(showgrid=False, gridwidth=1, gridcolor='black')
        fig4.update_yaxes(showgrid=False, gridwidth=1, gridcolor='black')
        fig4.update_yaxes(title_text="<b>Notes", dtick = 2, range = [0,10])
        fig4.update_xaxes(title_text="<b>Années", linecolor = 'rgba(0,0,0,0)')
        
        st.write(fig4)


    # Graph 6 (liste)
    
    st.subheader("Les films les mieux notés sur la période choisie:")
    top_notes2 = filtered_data[filtered_data['numVotes'] > 5000]
    top_notes_sorted1 = top_notes2.sort_values(
        'averageRating', ascending=False)
    top_10 = top_notes_sorted1.head(10)

    for i in range(1, 11, 1):
        st.write(str(i), '.', top_10['title'].iloc[i-1],
                 '(note :', str(top_10['averageRating'].iloc[i-1]), ')')

elif choice == 'Les acteurs dans le cinéma':

    st.markdown("""  <style> .reportview-container { background:
    url("https://wallpaperaccess.com/full/2300291.jpg")}
    </style> """, unsafe_allow_html=True)

    # On paramètre notre slider qui sert à choisir la période que l'on souhaite étudier
    years = []
    for i in range(2020, 1969, -1):
        years.append(i)
    year_to_filter = st.select_slider('Choisissez la période à étudier:',options=years)
    filtered_data = df_bases_filmsFR[df_bases_filmsFR['startYear']
                                     >= year_to_filter]
    filtered_data2 = df_acteurs_visu[(df_acteurs_visu['startYear'] >= year_to_filter)
                                     & ((df_acteurs_visu['category'].str.contains('act')))]

    # Graph (tableau) 1
    st.subheader("Les 10 acteurs les plus représentés:")
    st.markdown("***")

    # on établit le classement des 10 acteurs les plus présents
    classement = filtered_data2["primaryName"].value_counts().iloc[:10]

    # on nomme les colonnes de notre df
    classement = classement.reset_index()
    classement.columns = ['Acteurs', 'Nb films']

    classement2 = classement  # les 10 premiers pour les noms
    classement = classement.iloc[:3]  # les 3 premiers pour les images

    # on créer un nouveau df avec une seul occurence par acteurs
    df_bases_acteur_visu2 = filtered_data2.drop_duplicates(subset=[
                                                           'primaryName'])

    # on join les deux tables pour avoir le lien image avec le nom de l'acteur
    c_final = classement.merge(
        df_bases_acteur_visu2, left_on='Acteurs', right_on='primaryName', how='left')

    # On récupère l'image via le lien
    c_final['visu'] = c_final['lien_image'].apply(
        lambda x: link_preview(x).image)

    # On affiche le nom + l'image

    col1, col2, col3 = st.beta_columns(3)

    with col1:
        st.write(str(1), '.', c_final['Acteurs'].iloc[0])
        st.write(':clapper:',str(c_final['Nb films'].iloc[0]), 'films')
        st.image(c_final['visu'].iloc[0], width=200)
        url_1 = c_final['lien_image'].iloc[0]
        if st.button('En savoir plus'):webbrowser.open_new_tab(url_1)

    with col2:
        st.write(str(2), '.', c_final['Acteurs'].iloc[1])
        st.write(':clapper:',str(c_final['Nb films'].iloc[1]), 'films')
        st.image(c_final['visu'].iloc[1], width=200)
        url_2 = c_final['lien_image'].iloc[1]
        if st.button('En savoir plus '):webbrowser.open_new_tab(url_2)

    with col3:
        st.write(str(3), '.', c_final['Acteurs'].iloc[2])
        st.write(':clapper:',str(c_final['Nb films'].iloc[2]), 'films')
        st.image(c_final['visu'].iloc[2], width=200)
        url_3 = c_final['lien_image'].iloc[2]
        if st.button('En savoir plus  '):webbrowser.open_new_tab(url_3)

    st.markdown("***")

    #st.subheader('La suite du classement :')
    # for i in range(4, 11):
    #     st.write(str(i), '.', classement2['Acteurs'].iloc[i-1],
    #              ',', str(classement2['Nb films'].iloc[i-1]), 'films')

    # On récupère la colonne averageRating pour avoir les notes des films
    df_bases_acteurs_note = df_acteurs_visu[(df_acteurs_visu['startYear'] >= year_to_filter)]
    df_bases_acteurs_note = df_bases_acteurs_note.merge(df_bases_filmsFR, left_on='tconst', right_on='tconst', how='inner')
    df_bases_acteurs_note = df_bases_acteurs_note.drop(['startYear_y', 'genres_y', 'title_y', 'startYear_y'], axis = 1)
    df_bases_acteurs_note = df_bases_acteurs_note[df_bases_acteurs_note['category'].str.contains('act')]
    df_bases_acteurs_note.rename(columns={'genres_x': 'genres', 'title_x': 'title', 'startYear_x': 'startYear'}, inplace=True)

    # On crée une pivot table pour calculer la moyenne des notes et une autre pour le nombre de films
    data_pivot1 = pd.DataFrame(df_bases_acteurs_note.pivot_table(values = ['averageRating', 'numVotes'], index = 'primaryName', aggfunc = 'mean'))
    data_pivot2 = pd.DataFrame(df_bases_acteurs_note.pivot_table(values = ['title'], index = 'primaryName', aggfunc = 'count'))

    # On fusionne ces 2 pivot tables dans un dataframe pour avoir les infos notes et nb films pour chaque acteur :
    all_data = data_pivot1.merge(data_pivot2, left_on='primaryName', right_on='primaryName', how='inner')
    all_data = all_data.reset_index()
    # Top 10 en nombre de films :
    all_data_title = all_data.sort_values('title', ascending=False)
    all_data_title['rank'] = all_data_title['title'].rank(ascending=False).astype(int)
    all_data_title['acteurs'] = all_data_title['rank'].astype(str) + ". " + all_data_title['primaryName'] + "  "
    all_data_title = all_data_title[3:10]

    # Top 10 en moyenne de notes :
    all_data = all_data[all_data['title'] > all_data['title'].max()/4]
    all_data_note = all_data.sort_values('averageRating', ascending=False)
    all_data_note['rank'] = all_data_note['averageRating'].rank(ascending=False).astype(int)
    all_data_note['acteurs'] = all_data_note['rank'].astype(str) + ". " + all_data_note['primaryName'] + "  "
    all_data_note = all_data_note.head(10)

    fig, ax = plt.subplots(figsize=(15, 20))
    
    fig11 = px.bar(all_data_title, x='title', y='acteurs', color='title', text="title", height=400, color_continuous_scale=px.colors.sequential.Teal, orientation='h')
    fig11.layout.coloraxis.showscale = False
    fig11.update_layout(yaxis={'categoryorder':'total ascending'}, title='<b>La suite du classement</b>',
                       title_x=0.5, title_font_family="Verdana")                      
    fig11.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig11.update_layout(uniformtext_minsize=14, uniformtext_mode='hide')
    fig11.update_layout( yaxis = dict( tickfont = dict(size=16)))
    fig11.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
                       'paper_bgcolor': 'rgba(0,0,0,0)', })
    #fig11.update_yaxes(range=[5,8.5])
    #fig11.update_yaxes(tick0=0, dtick=0.5)
    fig11.update_xaxes(title_text="Nb Films")
    fig11.update_yaxes(title_text="")
    
    fig11.update_xaxes(showgrid=False, gridwidth=1, gridcolor='black')
    fig11.update_yaxes(showgrid=False, gridwidth=1, gridcolor='black')

    st.write(fig11) 

    fig12 = px.bar(all_data_note, x='averageRating', y='acteurs', color='averageRating', text="averageRating", height=400, color_continuous_scale=px.colors.sequential.Teal, orientation='h')
    fig12.layout.coloraxis.showscale = False
    fig12.update_layout(yaxis={'categoryorder':'total ascending'}, title='<b>Acteurs les mieux notés</b>',
                       title_x=0.5, title_font_family="Verdana")
    fig12.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig12.update_layout(uniformtext_minsize=14, uniformtext_mode='hide')
    fig12.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)',
                       'paper_bgcolor': 'rgba(0,0,0,0)', })
    fig12.update_xaxes(range=[5,8.5])
    fig12.update_xaxes(tick0=0, dtick=0.5)
    fig12.update_layout(yaxis = dict( tickfont = dict(size=16)))
    fig12.update_xaxes(title_text="Notes moyennes")
    fig12.update_yaxes(title_text="")
    fig12.update_xaxes(showgrid=False, gridwidth=1, gridcolor='black')
    fig12.update_yaxes(showgrid=False, gridwidth=1, gridcolor='black')

    st.write(fig12)

    

elif choice == "Le top 10":
    st.markdown("""  <style> .reportview-container { background:
    url("https://wallpaperaccess.com/full/2300291.jpg")}
    </style> """, unsafe_allow_html=True)

    #création de la selectbox "année"
    years = []
    for i in range(2020, 1969, -1):
        years.append(i)
    options = st.selectbox('Selectionner une année:', years)
    st.markdown("***")
    
    top_notes = df_bases_visu[df_bases_visu['numVotes'] > 5000]
    top_notes_sorted = top_notes.sort_values('averageRating', ascending=False)
    top_notes_by_year = top_notes_sorted[top_notes_sorted['startYear'] == options]
    top_10 = top_notes_by_year.head(10)
    top_3 = top_notes_by_year.head(3)

    # on va récuperer les images via les liens imbd
    
    top_3['visu'] = top_3['lien_image'].apply(lambda x: link_preview(x).image)
    

    col1, col2, col3 = st.beta_columns(3)
    with col1:
        st.write(str(1), '.', top_3['title'].iloc[0])
        st.write(':star: note :', str(top_3['averageRating'].iloc[0]), '/10')
        st.image(top_3['visu'].iloc[0], width=200)
        url_1 = top_3['lien_image'].iloc[0]
        if st.button('Bande-annonce'):webbrowser.open_new_tab(url_1)

    with col2:
        st.write(str(2), '.', top_3['title'].iloc[1])
        st.write(':star: note :', str(top_3['averageRating'].iloc[1]), '/10')
        st.image(top_3['visu'].iloc[1], width=200)
        url_2 = top_3['lien_image'].iloc[1]
        if st.button('Bande-annonce '):webbrowser.open_new_tab(url_2)

    with col3:
        st.write(str(3), '.', top_3['title'].iloc[2])
        st.write(':star: note :', str(top_3['averageRating'].iloc[2]), '/10')
        st.image(top_3['visu'].iloc[2], width=200)
        url_3 = top_3['lien_image'].iloc[2]
        if st.button('Bande-annonce  '):webbrowser.open_new_tab(url_3)

    st.markdown("***")
    st.subheader('La suite du classement :')

    for i in range(4, 11, 1):
        st.write(str(i), '.', top_10['title'].iloc[i-1],
                 '(note :', str(top_10['averageRating'].iloc[i-1]), '/10)')

elif choice == 'Recommandations personnalisées':

    st.markdown("""  <style> .reportview-container { background:
    url("https://www.wallpapertip.com/wmimgs/52-521720_movie-theater-background-for-youtube-videos-slideshows-film.jpg");
    background-size: cover}
    </style> """, unsafe_allow_html=True)
    
    st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)
    st.markdown('<body class="p">Vous en avez assez de toujours regarder les même films?</body>', unsafe_allow_html=True)
    st.markdown('<body class="p">Essayez dès à présent notre nouveau système de recommandation !</body>', unsafe_allow_html=True)

    # icon("search")
    user_input = st.text_input("", "Saisissez un film...")
    user_input2 = user_input
    user_input2 = user_input2.strip()
    user_input2 = user_input2.lower()
    user_input2 = user_input2.replace(" ", "")
    user_input2 = user_input2.replace("''", "")
    user_input2 = user_input2.replace(",", "")
    user_input2 = user_input2.replace("-", "")
    user_input2 = user_input2.replace(".", "")
    user_input2 = user_input2.replace(";", "")
    user_input2 = user_input2.replace(":", "")
    user_input2 = user_input2.replace("  ", " ")
    user_input2 = user_input2.encode('ascii', errors='ignore').decode('utf-8')
    #button_clicked = st.button("OK")

    if user_input != 'Saisissez un film...' and user_input != '':
        if (df_bases_KNN_F['new title'] == user_input2).any():
            X = df_bases_KNN_F.drop(columns=['index', 'tconst', 'title', 'lien_image','new title'])
            y = df_bases_KNN_F['tconst']

            scaler = StandardScaler().fit(X)  # Standardisation
            X_scaled = scaler.transform(X)

            model = KNeighborsClassifier(n_neighbors=4) #Initialisation du model
            model.fit(X_bis, y)

            X_ter = df_bases_KNN_F[df_bases_KNN_F['new title'].isin([user_input2])] #Recherche dans la bdd de l'input
            
            resultat = voisins_final.iloc[X_ter.iloc[:, 0]] #On retourne les voisins
            
            e = df_bases_KNN_F.iloc[[resultat.iloc[0,1]]]['lien_image'].apply(lambda x: link_preview(x).image)
            f = df_bases_KNN_F.iloc[[resultat.iloc[0,2]]]['lien_image'].apply(lambda x: link_preview(x).image)
            g = df_bases_KNN_F.iloc[[resultat.iloc[0,3]]]['lien_image'].apply(lambda x: link_preview(x).image)

            col1, col2, col3 = st.beta_columns(3)

            with col1:
                #st.subheader('')
                st.markdown('<body class="p2">Recommandation 1 :</body>', unsafe_allow_html=True)
                d = df_bases_KNN_F.iloc[[resultat.iloc[0,1]]]['title'].tolist()
                annee = df_bases_KNN_F.iloc[[resultat.iloc[0,1]]]['startYear'].tolist()
                st.write(d[0],'(', str(annee[0]),')')
                st.image(e.iloc[0], width=200)
                url_1 = df_bases_KNN_F.iloc[[resultat.iloc[0,1]]]['lien_image'].tolist()
                if st.button('Bande-annonce'):webbrowser.open_new_tab(str(url_1[0]))

            with col2:
                st.markdown('<body class="p2">Recommandation 2 :</body>', unsafe_allow_html=True)
                d = df_bases_KNN_F.iloc[[resultat.iloc[0,2]]]['title'].tolist()
                annee = df_bases_KNN_F.iloc[[resultat.iloc[0,2]]]['startYear'].tolist()
                st.write(d[0],'(', str(annee[0]),')')
                st.image(f.iloc[0], width=200)
                url_2 = df_bases_KNN_F.iloc[[resultat.iloc[0,2]]]['lien_image'].tolist()
                if st.button('Bande-annonce '):webbrowser.open_new_tab(str(url_2[0]))

            with col3:
                st.markdown('<body class="p2">Recommandation 3 :</body>', unsafe_allow_html=True)
                d = df_bases_KNN_F.iloc[[resultat.iloc[0,3]]]['title'].tolist()
                annee = df_bases_KNN_F.iloc[[resultat.iloc[0,3]]]['startYear'].tolist()
                st.write(d[0],'(', str(annee[0]),')')
                st.image(g.iloc[0], width=200)
                url_3 = df_bases_KNN_F.iloc[[resultat.iloc[0,3]]]['lien_image'].tolist()
                if st.button('Bande-annonce  '):webbrowser.open_new_tab(str(url_3[0]))

        else:
            name = df_bases_KNN_F[df_bases_KNN_F['new title'].str.contains(user_input2)]
            name_2 = name.iloc[:, 3].tolist()
            name_2.insert(0,'')
            options_f = st.selectbox('Choisissez dans la liste:', name_2, 
            format_func=lambda x: 'Choisissez dans la liste:' if x == '' else x)

            if options_f != '' :
                X = df_bases_KNN_F.drop(columns=['index', 'tconst', 'title', 'lien_image', 'new title'])
                y = df_bases_KNN_F['tconst']

                scaler = StandardScaler().fit(X)  # Standardisation
                X_scaled = scaler.transform(X)

                model = KNeighborsClassifier(n_neighbors=4)
                model.fit(X_bis, y)

                X_ter = df_bases_KNN_F[df_bases_KNN_F['title'].isin([options_f])]

                resultat = voisins_final.iloc[X_ter.iloc[:, 0]]

                col1, col2, col3 = st.beta_columns(3)

                e = df_bases_KNN_F.iloc[[resultat.iloc[0,1]]]['lien_image'].apply(lambda x: link_preview(x).image)
                f = df_bases_KNN_F.iloc[[resultat.iloc[0,2]]]['lien_image'].apply(lambda x: link_preview(x).image)
                g = df_bases_KNN_F.iloc[[resultat.iloc[0,3]]]['lien_image'].apply(lambda x: link_preview(x).image)

                col1, col2, col3 = st.beta_columns(3)

                with col1:
                    st.markdown('<body class="p2">Recommandation 1 :</body>', unsafe_allow_html=True)
                    d = df_bases_KNN_F.iloc[[resultat.iloc[0,1]]]['title'].tolist()
                    annee = df_bases_KNN_F.iloc[[resultat.iloc[0,1]]]['startYear'].tolist()
                    st.write(d[0],'(', str(annee[0]),')')
                    st.image(e.iloc[0], width=200)

                with col2:
                    st.markdown('<body class="p2">Recommandation 2 :</body>', unsafe_allow_html=True)
                    d = df_bases_KNN_F.iloc[[resultat.iloc[0,2]]]['title'].tolist()
                    annee = df_bases_KNN_F.iloc[[resultat.iloc[0,2]]]['startYear'].tolist()
                    st.write(d[0],'(', str(annee[0]),')')
                    st.image(f.iloc[0], width=200)

                with col3:
                    st.markdown('<body class="p2">Recommandation 3 :</body>', unsafe_allow_html=True)
                    d = df_bases_KNN_F.iloc[[resultat.iloc[0,3]]]['title'].tolist()
                    annee = df_bases_KNN_F.iloc[[resultat.iloc[0,3]]]['startYear'].tolist()
                    st.write(d[0],'(', str(annee[0]),')')
                    st.image(g.iloc[0], width=200)
            else:
                st.warning("Pas d'option sélectionnée !")

elif choice == "Suggestion de films":
    st.write("")
    st.markdown("""  <style> .reportview-container { background:
    url("https://wallpaperaccess.com/full/2300291.jpg")}
    </style> """, unsafe_allow_html=True)
    st.write("")
    st.write("")
    st.write("")
    st.markdown("<p class = 'p'>En manque d'inspiration ? Laissez vous guider par notre outil !</p>", unsafe_allow_html=True) 
    st.write("")

    df_bases_filmsFR_bis = df_bases_visu
    df_bases_filmsFR_bis.genres=df_bases_filmsFR_bis["genres"].apply(lambda x:x.split(","))
    liste_reco = df_bases_filmsFR_bis.explode("genres")
    
    def translate(x):
        translation = {'Comedy': 'Comédie', 'Fantasy': 'Fantastique', 'Romance': "Romance", 'Drama':'Drame', 'War':'Guerre',
                 'Musical': 'Musique', 'Action': 'Action', 'Crime': "Crime", 'Horror':'Horreur', 'Mystery':'Mystère',
                 'Adventure': 'Aventure', 'Thriller': 'Policier', 'Sci-Fi': "Sci-Fi", 'Western':'Western', 'History':'Historique',
                 'Biography': 'Biographie', 'Animation': 'Animation', 'Music': "Musique", 'Family':'Famille', 'Sport':'Sport',
                 'Documentary' : 'Documentaire'}
        for i in translation:
            y=translation.get(x, x)
            return y
    liste_reco['genres'] = liste_reco['genres'].apply(translate)

    df_bases_filmsFR_bis2 = df_bases_visu
    index_with_nan = df_bases_filmsFR_bis2.index[df_bases_filmsFR_bis2.isnull().any(axis=1)]
    df_bases_filmsFR_bis2.drop(index_with_nan,0, inplace=True)
    df_bases_filmsFR_bis2.country=df_bases_filmsFR_bis2["country"].apply(lambda x:x.split(","))
    liste_reco_country = df_bases_filmsFR_bis2.explode("country")
    liste_reco_country['country'] = liste_reco_country['country'].str.replace(" ","")
    
    liste_reco_country['country'] = liste_reco_country['country'].apply(translate_c)
    liste_reco['country'] = liste_reco['country'].apply(translate_c)
    

    liste_genre = liste_reco['genres'].unique().tolist()
    choix_genre = st.selectbox('Selectionnez un genre', liste_genre)

    my_expander = st.beta_expander('Plus de critères')
    with my_expander:
        years_2 = []
        for i in range(2020, 1969, -1):
            years_2.append(i)

        choix_annee = st.select_slider('Choisissez la période à étudier:', options=years_2)

        liste_pays = liste_reco_country['country'].unique().tolist()
        liste_pays.insert(0,'Tous')
        choix_pays = st.selectbox('Selectionnez un pays', liste_pays[0:20])

    if choix_pays != 'Tous':
        liste_reco_f = liste_reco[(liste_reco['genres']== choix_genre)
                                & (liste_reco['startYear'] >= choix_annee) 
                                & (liste_reco['country'] == choix_pays)
                                &(liste_reco['numVotes'] >5000)]

        liste_reco_f = liste_reco_f.sort_values('averageRating',ascending=False).head(3)
        
        liste_reco_f['visu'] = liste_reco_f['lien_image'].apply(lambda x: link_preview(x).image)
        st.markdown("***")
        
        col1, col2, col3 = st.beta_columns(3)
        with col1:
            st.write(str(1), '.', liste_reco_f['title'].iloc[0])
            st.image(liste_reco_f['visu'].iloc[0], width=200)
            url_1 = liste_reco_f['lien_image'].iloc[0]
            if st.button('Bande-annonce'):webbrowser.open_new_tab(url_1)

        with col2:
            st.write(str(2), '.', liste_reco_f['title'].iloc[1])
            st.image(liste_reco_f['visu'].iloc[1], width=200)
            url_2 = liste_reco_f['lien_image'].iloc[1]
            if st.button('Bande-annonce '):webbrowser.open_new_tab(url_2)

        with col3:
            st.write(str(3), '.', liste_reco_f['title'].iloc[2])
            st.image(liste_reco_f['visu'].iloc[2], width=200)
            url_3 = liste_reco_f['lien_image'].iloc[2]
            if st.button('Bande-annonce  '):webbrowser.open_new_tab(url_3)
        
    else:

        liste_reco_f = liste_reco[(liste_reco['genres']== choix_genre)
                                & (liste_reco['startYear'] >= choix_annee) 
                                &(liste_reco['numVotes'] >5000)]

        liste_reco_f = liste_reco_f.sort_values('averageRating',ascending=False).head(3)
        
        liste_reco_f['visu'] = liste_reco_f['lien_image'].apply(lambda x: link_preview(x).image)
        st.markdown("***")
        
        col1, col2, col3 = st.beta_columns(3)
        with col1:
            st.write(str(1), '.', liste_reco_f['title'].iloc[0])
            st.image(liste_reco_f['visu'].iloc[0], width=200)
            url_1 = liste_reco_f['lien_image'].iloc[0]
            if st.button('Bande-annonce'):webbrowser.open_new_tab(url_1)

        with col2:
            st.write(str(2), '.', liste_reco_f['title'].iloc[1])
            st.image(liste_reco_f['visu'].iloc[1], width=200)
            url_2 = liste_reco_f['lien_image'].iloc[1]
            if st.button('Bande-annonce '):webbrowser.open_new_tab(url_2)

        with col3:
            st.write(str(3), '.', liste_reco_f['title'].iloc[2])
            st.image(liste_reco_f['visu'].iloc[2], width=200)
            url_3 = liste_reco_f['lien_image'].iloc[2]
            if st.button('Bande-annonce  '):webbrowser.open_new_tab(url_3)

elif choice == 'Nos soirées spéciales':

    st.markdown("""  <style> .reportview-container { background:
    url("https://www.wallpaperuse.com/wallp/15-155709_m.jpg");
        background-size: cover;
    }}
    </style> """, unsafe_allow_html=True)

    

    st.write("")
    st.write("")
    st.write("")
    st.markdown("<p class = 'p3'>Nos soirées spéciales cinéma</p>", unsafe_allow_html=True)
    st.write("")
    st.markdown("<p class = 'p4'>Afin de célébrer la réouverture de notre cinéma, nous vous proposons de revivre chaque mois le meilleur du cinéma de ces 5 dernières décennies !</p>", unsafe_allow_html=True)
    st.markdown("<p class = 'p4'>Retrouvez nous chaque premier samedi du mois pour suivre cette programmation inédite.</p>", unsafe_allow_html=True)

    st.markdown("***")

    

    st.markdown("<p class = 'p'>Années 70: Le Parrain (1972)</p>", unsafe_allow_html=True)
    st.markdown("<p class = 'p1'>Le samedi 22 Mai à 20h00</p1>", unsafe_allow_html=True) 

    col1, col2, col3 = st.beta_columns(3)

    with col1:
        st.write("")

    with col2:
        st.image('https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_UY1200_CR107,0,630,1200_AL_.jpg', width=200)
        url_1 = "https://www.imdb.com/title/tt0068646/"
        if st.button('Bande-annonce'):webbrowser.open_new_tab(url_1)
        st.button('  Réserver la séance  ')


    with col3:
        st.write("")
   
    st.markdown("***")

    st.markdown("<p class = 'p'>Années 80: Star Wars: Épisode V - L'Empire contre-attaque (1980)</p>", unsafe_allow_html=True)
    st.markdown("<p class = 'p1'>Le samedi 05 Juin à 20h00</p1>", unsafe_allow_html=True)   
    
    col1, col2, col3 = st.beta_columns(3)

    with col1:
        st.write("")

    with col2:
        st.image("https://m.media-amazon.com/images/M/MV5BYmU1NDRjNDgtMzhiMi00NjZmLTg5NGItZDNiZjU5NTU4OTE0XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_UY1200_CR70,0,630,1200_AL_.jpg", width=200)
        url_2 = "https://www.imdb.com/title/tt0080684/"
        if st.button('Bande-annonce '):webbrowser.open_new_tab(url_2)
        st.button('  Réserver la séance ')
    with col3:
        st.write("")
    
    st.markdown("***")
    st.markdown("<p class = 'p'>Années 90: Les Évadés (1994)</p>", unsafe_allow_html=True)
    st.markdown("<p class = 'p1'>Le samedi 03 Juillet à 20h00</p1>", unsafe_allow_html=True)   
    
    col1, col2, col3 = st.beta_columns(3)

    with col1:
        st.write("")

    with col2:
        st.image("https://m.media-amazon.com/images/M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_UY1200_CR89,0,630,1200_AL_.jpg", width=200)
        url_3 = "https://www.imdb.com/title/tt0111161/?ref_=fn_al_tt_1"
        if st.button(' Bande-annonce '):webbrowser.open_new_tab(url_3)
        st.button(' Réserver la séance ')
    with col3:
        st.write("")

    st.markdown("***")

    st.markdown("<p class = 'p'>Années 2000: The Dark Knight : Le Chevalier noir (2008)</p>", unsafe_allow_html=True)
    st.markdown("<p class = 'p1'>Le samedi 07 Août à 20h00</p1>", unsafe_allow_html=True)   
    
    col1, col2, col3 = st.beta_columns(3)

    with col1:
        st.write("")

    with col2:
        st.image("https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_UY1200_CR90,0,630,1200_AL_.jpg", width=200)
        url_4 = "https://www.imdb.com/title/tt0468569/?ref_=nv_sr_srsg_0"
        if st.button('  Bande-annonce '):webbrowser.open_new_tab(url_4)
        st.button('Réserver la séance ')
    with col3:
        st.write("")

    st.markdown("***")

    st.markdown("<p class = 'p'>Années 2010: Interstellar (2014)</p>", unsafe_allow_html=True)
    st.markdown("<p class = 'p1'>Le samedi 04 Septembre à 20h00</p1>", unsafe_allow_html=True)   
    
    col1, col2, col3 = st.beta_columns(3)

    with col1:
        st.write("")

    with col2:
        st.image("https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_UY1200_CR90,0,630,1200_AL_.jpg", width=200)
        url_5 = "https://www.imdb.com/title/tt0816692/?ref_=fn_al_tt_1"
        if st.button('  Bande-annonce  '):webbrowser.open_new_tab(url_5)
        st.button('Réserver la séance')
    with col3:
        st.write("")

elif choice == 'Nos tarifs':

    st.markdown("""  <style> .reportview-container { background:
    url("https://wallpaperaccess.com/full/2300291.jpg")}
    </style> """, unsafe_allow_html=True)

    st.write("")
    st.write("")
    st.write("")
    html_code = """

    <table class="styled-table" style = 'border-collapse: collapse; min-width: 400px;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0); background-color: transparent; color: #ffffff; text-align: center; padding:0; border-top: 1.5px #dddddd;
    border-bottom: 1.5px #dddddd; border-left: 1.5px solid #dddddd; border-right:1.5px #dddddd; width: 100%; height:100%; margin:0'>
    <thead style = 'font-weight: bold; font-family: verdana; font-size: 1.8em'>
        <tr style = 'border: 1.5px #dddddd'>
            <th></th>
            <th>Tarifs</th>
        </tr>
    </thead>
    <tbody>
        <tr class="active-row">
            <td class = "active-row">Plein tarif</td>
            <td class = "active-row2" style = 'border-left: 1.5px  #dddddd'>7,90 €</td>
        </tr>
        <tr class="active-row">
            <td class = "active-row">Tarif réduit</td>
            <td class = "active-row2" style = 'border-left: 1.5px #dddddd'>6,40 €</td>
        </tr>
        <tr class="active-row">
            <td class = "active-row">Tarif unique (mercredi)</td>
            <td class = "active-row2" style = 'border-left: 1.5px #dddddd'>5,90 €</td>
        </tr>
        <tr class="active-row">
            <td class = "active-row">Moins de 14 ans</td>
            <td class = "active-row2" style = 'border-left: 1.5px  #dddddd'>4 €</td>
        </tr>
        <tr class="active-row">
            <td class = "active-row">Tarif séniors</td>
            <td class = "active-row2" style = 'border-left: 1.5px  #dddddd'>6,40 €</td>
        </tr>
        <tr class="active-row">
            <td class = "active-row">Supplément scéance 3D</td>
            <td class = "active-row2" style = 'border-left: 1.5px #dddddd'>1 €</td>
        </tr>
       <tr class="active-row">
            <td class = "active-row">Abonnement 5 places (valables 6 mois)</td>
            <td class = "active-row2" style = 'border-left: 1.5px  #dddddd'>32 €</td>
        </tr>
       <tr class="active-row">
            <td class = "active-row">Formule Duo (2 films vus le même jour)</td>
            <td class = "active-row2" style = 'border-left: 1.5px  #dddddd'>10 €</td>
        </tr>
    </tbody>
    </table>
    """

    st.markdown(html_code, unsafe_allow_html=True)

    col1, col2 = st.beta_columns(2)

    with col1 :
        st.header("")
        st.image("https://cdn4.cobra.fr/25609/600x315/les-tv-et-videoprojecteurs-certifies-thx.jpg", width=210)
        
    with col2 :
        st.header("")
        st.image("https://logos-world.net/wp-content/uploads/2020/12/Dolby-Digital-Emblem.png", width=250)

elif choice == 'Nous contacter':
    st.markdown("""  <style> .reportview-container { background:
    url("https://wallpapercave.com/wp/wp3157716.jpg")}
    </style> """, unsafe_allow_html=True)

    st.subheader("Nos coordonnées:")
    st.write("Adresse : 1 Rue du Sénéchal, 23000 Guéret")
    st.write(":telephone_receiver: Téléphone: 05 85 52 26 44")
    st.write(":email: E-mail : cinemalecreusois@gmail.com")
    st.subheader("Nous trouver:")
    data = pd.DataFrame({'awesome cities': ['Guéret'], 'lat': [
                        46.169599], 'lon': [1.871452]})
    st.map(data)
    st.subheader(":pencil2: Nous écrire:")
    st.text_area('', height=100)
    st.button('Envoyer')
