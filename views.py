import datetime
from flask import Flask, render_template, request, redirect
import mysql.connector
from main import app
import pyodbc

db_config = {
    'host': 'localhost',
    'user': 'haoyu',
    'password': 'jiafang',
    'database': 'haoyugiegie'
}

def get_analyticdb_connection():
    server = 'gp-2zebk63jlt975um7h-master.gpdb.rds.aliyuncs.com'
    database = 'haoyu'
    username = 'junic'
    password = 'Aa123456'
    driver = '{ODBC Driver 17 for SQL Server}'
    connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    conn = pyodbc.connect(connection_string)
    return conn

def get_db_connection():
    """Establishes and returns a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

@app.route('/')
@app.route('/home')
def index():
    """Renders the home page."""
    return render_template(
        'index.html',
        title="指望另一队 - 主页"
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title="指望另一队 - 联系我们"
    )

@app.route('/aboutus')
def aboutus():
    """Renders the aboutus page."""
    return render_template(
        'aboutus.html',
        title="指望另一队 - 开发历程"
    )

@app.route('/course')
def course():
    """Renders the course page."""
    return render_template(
        'course.html',
        title="指望另一队 - 选课建议"
    )

@app.route('/detail')
def detail():
    """Renders the coming-soon page."""
    return render_template(
        'detail.html',
        title="前方开发中"
    )

@app.route('/feedback')
def feedback():
    """Renders the feedback page with feedback from the database."""
    
    conn = get_db_connection()
    feedbacks = []

    if conn:
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT name, phone, email, message, created_at FROM feedback ORDER BY created_at DESC")
            feedbacks = cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

    return render_template(
        'feedback.html',
        title="指望另一队 - 在线留言",
        feedbacks=feedbacks
    )


@app.route('/food')
def food():
    """Renders the food page."""
    foods = [['财记甜铺', '5.0', '好吃的，清清爽爽的，食材很新鲜。'], ['切果NOW', '5.0', '特别好，水果新鲜好吃，很干净。'], 
             ['浆小白·豆浆夜市', '4.8', '好吃，量大，虾饺和包子皮都很薄，豆腐花很嫩滑。'], ['鸡柳大人', '4.6', '鸡柳酥脆年糕软糯，性价比高，甜甜辣辣的很好吃！'], 
             ['雄逗逗·福鼎肉片', '4.7', '牛肉劲道，汤很好喝。福鼎肉片挺好吃的，土豆比较油。'], ['淮南牛肉汤', '4.6', '牛肉粉丝汤配香酥饼很好吃，汤比较清淡，饼很脆。分量足。'], 
             ['厚厚吃希腊酸奶', '4.5', '好吃的！虽然希腊酸奶干干的没味道但是搭配着蜂蜜水果还是挺好吃的。分量比想象中小。'], 
             ['袁记云饺', '4.5', '食材新鲜，豆芽解腻，云吞馅多皮薄，好吃。'], ['阿佑鲜烫牛肉米线', '4.8', '粉很好吃，汤也很鲜，烫牛肉刚刚好，配上菜吃很好吃'], 
             ['千里香馄饨王', '5.0', '好吃，馄饨量比较少。'], ['老乡鸡', '4.8', '分量大，很好吃，价廉物美。'], ['大米先生', '4.8', '好吃，小炒肉很下饭。量比较少。'], 
             ['老盛昌汤包', '3.7', '老盛昌的味道始终如一，汤包皮薄馅多，汁水鲜美，入口即化，配上一碗热腾腾的馄饨，简直是完美搭配。环境整洁舒适，服务热情周到，性价比高。'], 
             ['逍遥镇胡辣汤', '4.8', '味道好，新鲜，量大。'], ['小杨生煎', '4.8', '服务很好，口味也很好，鸭血粉丝汤有家的味道。'], 
             ['和善圆·手工大包', '4.7', '鲜嫩多汁，皮软软的，热热的好吃。'], ['巴比馒头', '4.7', '包子皮比较厚，味道好吃。服务一般。'], 
             ['鱼你在一起', '4.4', '鱼很多，很入味，好吃。外卖鱼肉较少。'], ['宜德饭堂', '4.8', '环境不错，卫生挺好，口味偏清淡。'], 
             ['崔大人韩式炸鸡', '5.0', '好吃，速度快，外壳酥脆。'], ['牛约堡·手作牛肉汉堡', '4.2', '味道赞，分量足，口味独特，价格实惠，性价比高。'], 
             ['喜姐炸串', '4.8', '味道好，分量足，鸡腿大，外壳焦脆好吃。'], ['三米粥铺', '4.9', '粥满料足，小吃好吃。'], ['麦当劳', '5.0', '谁能不爱。']]
    group = (datetime.date.today()-datetime.date(2024, 1, 1)).days%24//6
    return render_template(
        'food.html',
        title="指望另一队 - 美食推荐",
        food1='\t\t'.join(foods[group*4]),
        food2='\t\t'.join(foods[group*4+1]),
        food3='\t\t'.join(foods[group*4+2]),
        food4='\t\t'.join(foods[group*4+3])
    )

@app.route('/francais')
def francais():
    """Renders the francais page."""
    phrases = ["Crois en toi-même et tout devient possible.", "Chaque jour est une nouvelle opportunité pour réussir.", "Les défis sont des opportunités déguisées.", 
               "Tu es plus fort(e) que tu ne le crois.", "Ne laisse jamais tomber tes rêves.", "Le succès est la somme de petits efforts répétés chaque jour.", 
               "Même la plus longue des routes commence par un premier pas.", "Tout problème a une solution, il suffit de la trouver.", "La persévérance est la clé du succès.", 
               "L'échec est simplement une étape vers la réussite.", "Apprends d’hier, vis aujourd’hui et espère pour demain.", 
               "La force intérieure te guide vers tes objectifs.", "Ne te compare pas aux autres, avance à ton rythme.", "La confiance en soi est le premier secret du succès.", 
               "Ce n’est pas parce que c’est difficile que tu n’y arriveras pas.", "Transforme tes faiblesses en forces.", "Sois fier(e) de chaque petit progrès que tu fais.", 
               "Tu es capable de surmonter n'importe quel obstacle.", "Reste positif(ve), même dans les moments difficiles.", 
               "Les grandes choses prennent du temps, sois patient(e).", "La clé de la réussite est de ne jamais abandonner.", "Tu es maître(se) de ton destin.", 
               "Ton potentiel est infini, crois-y.", "La vie récompense ceux qui persévèrent.", "Chaque erreur est une leçon précieuse.", 
               "Souris à la vie, et elle te sourira en retour.", "Ton travail acharné portera ses fruits.", "Ce que tu fais aujourd’hui peut améliorer ton avenir.", 
               "La volonté trouve toujours un chemin.", "Rien n'est impossible pour celui ou celle qui croit.", "Les efforts constants mènent aux grandes réalisations.", 
               "Aie foi en toi et en tes capacités.", "Chaque petit pas te rapproche de ton but.", "L'échec est un tremplin pour le succès.", 
               "La persévérance transforme les rêves en réalité.", "Ne sous-estime jamais ta force intérieure.", 
               "L’important n’est pas la vitesse, mais de ne jamais s’arrêter.", "Continue à avancer, même lorsque c'est difficile.", "Ton attitude détermine ton altitude.", 
               "Le courage est la moitié de la victoire.", "L’optimisme est la clé pour voir la lumière dans l’obscurité.", 
               "Les rêves deviennent réalité pour ceux qui osent y croire.", "Chaque défi que tu relèves te rend plus fort(e).", 
               "Ne te laisse pas décourager par les obstacles.", "Rappelle-toi toujours pourquoi tu as commencé.", "Tu es plus proche de ton but que tu ne le penses.", 
               "La patience et la persévérance triomphent toujours.", "Le succès commence par une pensée positive.", "Le seul échec est d’abandonner.", 
               "Rêve en grand, travaille dur, reste humble.", "Ton avenir dépend des choix que tu fais aujourd'hui.", "Chaque jour est une chance de recommencer.", 
               "La foi en toi est ton meilleur allié.", "La clé du succès est de commencer maintenant.", "Fais confiance au processus, les résultats viendront.", 
               "Un esprit positif attire des choses positives.", "Les difficultés d’aujourd’hui sont les victoires de demain.", 
               "La discipline est le pont entre les objectifs et les accomplissements.", "Ton potentiel est plus grand que tes peurs.", 
               "La persévérance finit toujours par payer.", "Les grandes réalisations commencent par un simple acte de courage.", 
               "Apprends de tes erreurs, mais ne les laisse pas te définir.", "Le courage est de continuer même quand on a peur.", 
               "Ta force réside dans ta capacité à ne jamais abandonner.", "La réussite est un voyage, pas une destination.", 
               "Chaque petit pas compte dans la bonne direction.", "Le bonheur se trouve dans les efforts que tu fais.", 
               "Les rêves sont faits pour être réalisés, pas pour être oubliés.", "La confiance est la moitié de la victoire.", 
               "Chaque jour est une opportunité d’être meilleur(e).", "Les grandes choses naissent de petits débuts.", 
               "Tu es exactement là où tu dois être pour réussir.", "Le succès sourit à ceux qui persévèrent.", "Tout ce que tu veux est de l'autre côté de la peur.", 
               "Les échecs sont des leçons déguisées.", "Si tu peux le rêver, tu peux le réaliser.", "Ton futur dépend de ce que tu fais aujourd’hui.", 
               "Les limites n'existent que dans ton esprit.", "Ne laisse jamais personne te dire que tu ne peux pas réussir.", "Chaque jour est une chance de progresser.", 
               "Tu es unique et irremplaçable.", "Rien de grand n’a jamais été accompli sans passion.", "Tu es plus résilient(e) que tu ne l’imagines.", 
               "L’important, c’est de continuer à avancer.", "Les obstacles ne sont que des étapes sur le chemin du succès.", 
               "Fais de tes rêves une réalité, pas une simple idée.", "Crois en tes capacités, elles te porteront loin.", "Chaque fin est un nouveau commencement.", 
               "L’avenir appartient à ceux qui croient en la beauté de leurs rêves.", "Chaque épreuve te rend plus fort(e) et plus sage.", 
               "Tu es plus proche de ton but que tu ne le crois.", "Sois patient(e), les grandes choses prennent du temps.", "Ton potentiel est illimité.",
               "Le succès est le résultat d’un travail constant."
               ]
    return render_template(
        'francais.html',
        title="指望另一队 - 法语学习",
        francais_text=datetime.date.today().strftime('%Y-%m-%d')+"每日一句:  "+phrases[(datetime.date.today()-datetime.date(2024, 1, 1)).days%94]
    )

@app.route('/submit', methods=['POST'])
def submit_feedback():
    """Handles the form submission and renders a thank-you page with the submitted data."""
    
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        message = request.form['message']
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()

            try:
                cursor.execute("""
                    INSERT INTO feedback (name, phone, email, message)
                    VALUES (%s, %s, %s, %s)
                """, (name, phone, email, message))

                conn.commit()
            except Exception as e:
                print(f"Error: {e}")
                conn.rollback()
            finally:
                cursor.close()
                conn.close()
        
        return render_template(
            'thankyou.html',
            title="感谢您的反馈",
            name=name,
            phone=phone,
            email=email,
            message=message
        )

@app.route('/project')
def project():
    """Renders the project page."""
    return render_template(
        'project.html',
        title="指望另一队 - 项目简介"
    )

@app.route('/s1')
def s1():
    """Renders the s1 page."""
    return render_template(
        's1.html',
        title="指望另一队 - 开发历程"
    )

@app.route('/s2')
def s2():
    """Renders the s2 page."""
    return render_template(
        's2.html',
        title="指望另一队 - 开发历程"
    )

@app.route('/s3')
def s3():
    """Renders the s3 page."""
    return render_template(
        's3.html',
        title="指望另一队 - 开发历程"
    )

@app.route('/s4')
def s4():
    """Renders the s4 page."""
    return render_template(
        's4.html',
        title="指望另一队 - 开发历程"
    )
