import os, sqlite3, requests, streamlit as st
from urllib.parse import quote
st.set_page_config(page_title="CineMatch",page_icon="🎬",layout="wide")
DB=os.path.join(os.path.dirname(__file__),"cinematch.db")
TOKEN=os.getenv("TMDB_READ_TOKEN","").strip()
SEED=[
("The Godfather",1972,"🇺🇸 الولايات المتحدة","مافيا، جريمة، دراما","عائلة إجرامية نافذة تواجه أزمة خلافة تسحب أصغر أبنائها إلى عالم كان يريد الابتعاد عنه.",9.2,"tt0068646"),
("Goodfellas",1990,"🇺🇸 الولايات المتحدة","مافيا، جريمة، سيرة","شاب ينجذب إلى عالم الجريمة المنظمة، حيث يصبح الولاء والطموح طريقًا محفوفًا بالخطر.",8.7,"tt0099685"),
("The Departed",2006,"🇺🇸 الولايات المتحدة","جريمة، تشويق، مخابرات","شرطي يتسلل إلى عصابة، ومجرم يعمل داخل الشرطة؛ وكل طرف يحاول كشف الآخر.",8.5,"tt0407998"),
("Scarface",1983,"🇺🇸 الولايات المتحدة","مافيا، طموح، جريمة","مهاجر طموح يصعد في عالم الجريمة بميامي، لكن جوعه للسلطة يهدد كل ما بناه.",8.3,"tt0086250"),
("Heat",1995,"🇺🇸 الولايات المتحدة","جريمة، تشويق، ذكاء","محقق دقيق ولص محترف يدخلان مواجهة استراتيجية عالية المخاطر.",8.3,"tt0113277"),
("Carlito's Way",1993,"🇺🇸 الولايات المتحدة","مافيا، دراما، جريمة","مجرم سابق يحاول بدء حياة جديدة، لكن علاقاته القديمة تهدد فرصته في الهروب من الماضي.",7.9,"tt0106519"),
("There Will Be Blood",2007,"🇺🇸 الولايات المتحدة","طموح، دراما، سلطة","منقّب نفط طموح يبني ثروة ضخمة، بينما تستهلكه الرغبة في السيطرة.",8.2,"tt0469494"),
("Whiplash",2014,"🇺🇸 الولايات المتحدة","تحفيزي، موسيقى، دراما","عازف طبول شاب يدخل علاقة قاسية مع مدرّب لا يرضى إلا بالكمال، فيختبر ثمن العظمة.",8.5,"tt2582802"),
("The Social Network",2010,"🇺🇸 الولايات المتحدة","أعمال، ذكاء، دراما","مشروع جامعي يتحول إلى شركة تغيّر العالم، بينما تتصادم الصداقة والطموح والملكية.",7.8,"tt1285016"),
("Moneyball",2011,"🇺🇸 الولايات المتحدة","أعمال، استراتيجية، رياضة","مدير فريق رياضي يتحدى الطرق التقليدية باستخدام البيانات لبناء فريق منافس بميزانية محدودة.",7.6,"tt1210166"),
("Good Will Hunting",1997,"🇺🇸 الولايات المتحدة","ذكاء، دراما، نضج","عامل نظافة موهوب رياضيًا يواجه ماضيه ليقرر كيف سيستخدم قدراته الاستثنائية.",8.3,"tt0119217"),
("Fight Club",1999,"🇺🇸 الولايات المتحدة","دراما، تشويق، هوية","موظف يعاني الأرق يلتقي رجلًا غامضًا وينجرف إلى حركة سرية تتجاوز السيطرة.",8.8,"tt0137523"),
("Se7en",1995,"🇺🇸 الولايات المتحدة","جريمة، غموض، تشويق","محققان يلاحقان قاتلًا ترتبط جرائمه بنمط أخلاقي مرعب.",8.6,"tt0114369"),
("The Shawshank Redemption",1994,"🇺🇸 الولايات المتحدة","دراما، أمل، صداقة","مصرفي محكوم عليه بالسجن المؤبد يبني صداقة طويلة ويتمسك بالأمل.",9.3,"tt0111161"),
("12 Angry Men",1957,"🇺🇸 الولايات المتحدة","دراما، محكمة، ذكاء","محلف واحد يشكك في حكم إدانة، فيجبر أحد عشر رجلًا على إعادة فحص الأدلة وتحيزاتهم.",9.0,"tt0050083"),
("City of God",2002,"🇧🇷 البرازيل","جريمة، نضج، دراما","صبيان يكبران في حي فقير بريو؛ أحدهما يطارد التصوير والآخر يسعى إلى السلطة عبر الجريمة.",8.6,"tt0317248"),
("Parasite",2019,"🇰🇷 كوريا الجنوبية","تشويق، دراما، سخرية اجتماعية","عائلة تعاني الفقر تتسلل تدريجيًا إلى حياة أسرة ثرية، فتبدأ عواقب غير متوقعة.",8.5,"tt6751668"),
("Seven Samurai",1954,"🇯🇵 اليابان","ملحمي، أكشن، دراما","قرية تستعين بمجموعة من الساموراي للدفاع عنها ضد قطاع الطرق.",8.6,"tt0047478"),
("Spirited Away",2001,"🇯🇵 اليابان","أنيميشن، فانتازيا، نضج","فتاة تدخل عالمًا غامضًا للأرواح وتحتاج إلى الشجاعة لإنقاذ عائلتها.",8.6,"tt0245429"),
("Cinema Paradiso",1988,"🇮🇹 إيطاليا","دراما، حنين، كلاسيكي","مخرج يتذكر سينما قريته والعامل الذي شكّل طفولته وحبه للأفلام.",8.5,"tt0095765"),
("Amélie",2001,"🇫🇷 فرنسا","رومانسي، كوميديا، خيال","نادلة خجولة في باريس تغيّر حياة من حولها بينما تتعلم ملاحقة سعادتها.",8.3,"tt0211915"),
("The Lives of Others",2006,"🇩🇪 ألمانيا","دراما، تشويق، مراقبة","عميل في ألمانيا الشرقية يراقب فنانين، لكنه يتورط عاطفيًا في الحياة التي يتجسس عليها.",8.4,"tt0405094"),
("The Pianist",2002,"🇵🇱 بولندا","سيرة، دراما، حرب","عازف بيانو يهودي بولندي يحاول النجاة من تدمير وارسو خلال الحرب العالمية الثانية.",8.5,"tt0253474"),
("A Separation",2011,"🇮🇷 إيران","دراما، عائلة، معضلة أخلاقية","انفصال زوجين يتحول إلى نزاع قانوني وأخلاقي تتداخل فيه العائلة والطبقة والحقيقة.",8.3,"tt1832382"),
("The Battle of Algiers",1966,"🇩🇿 الجزائر","حرب، تاريخ، سياسة","عمل بأسلوب شبه وثائقي يتناول نضال الاستقلال الجزائري ومواجهة السلطات الاستعمارية.",8.1,"tt0058946"),
("The Yacoubian Building",2006,"🇪🇬 مصر","دراما، مجتمع، قصص متشابكة","سكان عمارة في القاهرة تكشف حكاياتهم عن الطموح والطبقة والسياسة والصراع الشخصي.",7.5,"tt0421642"),
("Capernaum",2018,"🇱🇧 لبنان","دراما، اجتماعي","طفل يعيش ظروفًا قاسية يقاضي والديه، كاشفًا معاناة الأطفال المهمشين.",8.4,"tt8267604"),
("Wadjda",2012,"🇸🇦 السعودية","دراما، نضج","فتاة تحلم بامتلاك دراجة وتبحث عن طرق لتجاوز القيود المحيطة بها.",7.5,"tt2258858"),
("Theeb",2014,"🇯🇴 الأردن","مغامرة، دراما، نضج","فتى بدوي يخوض رحلة صحراوية خطرة خلال الحرب العالمية الأولى.",7.2,"tt3170902"),
("3 Idiots",2009,"🇮🇳 الهند","كوميديا، دراما، تعليم","ثلاثة طلاب هندسة يواجهون ضغط الدراسة والصداقة ومعنى النجاح.",8.4,"tt1187043"),
("The Secret in Their Eyes",2009,"🇦🇷 الأرجنتين","جريمة، غموض، رومانسية","محقق متقاعد يعود إلى قضية لم تُحل وتركت أثرًا عميقًا في حياته.",8.2,"tt1305806"),
("The Hunt",2012,"🇩🇰 الدنمارك","دراما، نفسي، مجتمع","حياة مدرس تنهار بعد سوء فهم ينتشر داخل مجتمع صغير.",8.3,"tt2106476"),
("The Raid",2011,"🇮🇩 إندونيسيا","أكشن، تشويق، فنون قتالية","فريق شرطة يجد نفسه محاصرًا في مبنى شاهق يسيطر عليه زعيم عصابة.",7.6,"tt1899353"),
("Inception",2010,"🇺🇸 الولايات المتحدة","خيال علمي، تشويق، ذكاء","متخصص في استخراج الأسرار من الأحلام يتلقى مهمة زرع فكرة بدلًا من سرقتها.",8.8,"tt1375666"),
("The Prestige",2006,"🇺🇸 الولايات المتحدة","غموض، تشويق، ذكاء","ساحران متنافسان يستهلكهما الصراع والسرية والسعي إلى الخدعة المثالية.",8.5,"tt0482571"),
("The Dark Knight",2008,"🇺🇸 الولايات المتحدة","أكشن، جريمة، أبطال خارقون","باتمان يواجه عقلًا إجراميًا يدفع مدينة جوثام إلى اختبار حدودها الأخلاقية.",9.0,"tt0468569"),
("The Matrix",1999,"🇺🇸 الولايات المتحدة","خيال علمي، أكشن، فلسفة","مبرمج يكتشف أن الواقع قد يكون نظامًا مصطنعًا وينضم إلى حركة مقاومة.",8.7,"tt0133093"),
("The Wolf of Wall Street",2013,"🇺🇸 الولايات المتحدة","سيرة، جريمة، أعمال","صعود سمسار أسهم في عالم الإفراط والاحتيال يكشف الجانب المدمر للطموح المنفلت.",8.2,"tt0993846"),
("Ford v Ferrari",2019,"🇺🇸 الولايات المتحدة","سيرة، رياضة، هندسة","شركة سيارات تجمع مصممًا مبتكرًا وسائقًا جريئًا لتحدي فيراري في سباق لومان.",8.1,"tt1950186"),
("Rush",2013,"🇬🇧 بريطانيا","سيرة، رياضة، منافسة","منافسان في الفورمولا 1، جيمس هانت ونيكي لاودا، يدفع كل منهما الآخر خلال موسم خطير.",8.1,"tt1979320"),
("Casino",1995,"🇺🇸 الولايات المتحدة","جريمة، مافيا، دراما","مدير كازينو بارع يواجه الفساد والطموح والخيانة في لاس فيغاس.",8.2,"tt0112641"),
("The Truman Show",1998,"🇺🇸 الولايات المتحدة","دراما، كوميديا، خيال علمي","رجل يبدأ في الشك بأن العالم المنظم حوله ليس كما يبدو.",8.2,"tt0120382"),
("Interstellar",2014,"🇺🇸 الولايات المتحدة","خيال علمي، دراما، فضاء","فريق يسافر خارج الأرض بحثًا عن مستقبل للبشرية، في اختبار للزمن وروابط الأسرة.",8.7,"tt0816692"),
("Gladiator",2000,"🇺🇸 الولايات المتحدة","ملحمي، أكشن، انتقام","قائد روماني يُخان ويُستعبد، ثم يقاتل في الحلبة سعيًا للانتقام.",8.5,"tt0172495"),
("The Grand Budapest Hotel",2014,"🇺🇸 الولايات المتحدة","كوميديا، مغامرة، جريمة","مدير فندق شهير ومساعده يتورطان في لوحة مسروقة وثروة عائلية وأوروبا المتغيرة.",8.1,"tt2278388"),
("Oldboy",2003,"🇰🇷 كوريا الجنوبية","تشويق، غموض، انتقام","رجل يُطلق سراحه بعد سنوات من الاحتجاز الغامض، فيبدأ بحثًا يائسًا عن إجابات.",8.3,"tt0364569"),
("The Intouchables",2011,"🇫🇷 فرنسا","كوميديا، دراما، صداقة","تنشأ صداقة غير متوقعة بين أرستقراطي ذي إعاقة ومساعده غير التقليدي.",8.5,"tt1675434"),
("The Seventh Seal",1957,"🇸🇪 السويد","دراما، فانتازيا، كلاسيكي","فارس عائد من الحروب الصليبية يلعب الشطرنج مع الموت بحثًا عن المعنى.",8.1,"tt0050976"),
("The Good, the Bad and the Ugly",1966,"🇮🇹 إيطاليا","ويسترن، مغامرة، كلاسيكي","ثلاثة مسلحين يعقدون تحالفات متوترة بحثًا عن ذهب مدفون خلال الحرب الأهلية الأمريكية.",8.8,"tt0060196"),
("The Message",1976,"🇱🇾 ليبيا","تاريخي، دراما، ملحمي","ملحمة تاريخية تتناول بدايات المجتمع الإسلامي عبر تجارب الشخصيات المحيطة بالأحداث.",8.1,"tt0074896"),
("The Square",2013,"🇪🇬 مصر","وثائقي، تاريخ","وثائقي يتابع ناشطين ومواطنين خلال تحولات الثورة المصرية.",8.0,"tt2486682")]
def db():
 c=sqlite3.connect(DB,check_same_thread=False);c.row_factory=sqlite3.Row
 c.execute("CREATE TABLE IF NOT EXISTS movies(id INTEGER PRIMARY KEY,title TEXT,year INTEGER,country TEXT,genres TEXT,overview TEXT,ref_rating REAL,imdb_id TEXT,tmdb_id INTEGER UNIQUE,poster_path TEXT)")
 c.execute("CREATE TABLE IF NOT EXISTS feedback(movie_id INTEGER PRIMARY KEY,liked INTEGER DEFAULT 0,rating INTEGER,status TEXT DEFAULT '',notes TEXT DEFAULT '')")
 if c.execute("SELECT COUNT(*) FROM movies").fetchone()[0]==0:
  c.executemany("INSERT INTO movies(title,year,country,genres,overview,ref_rating,imdb_id) VALUES(?,?,?,?,?,?,?)",SEED)
 c.commit();return c
def weights(c):
 out={}
 for r in c.execute("SELECT m.genres,f.liked,f.rating FROM movies m JOIN feedback f ON m.id=f.movie_id"):
  val=(2 if r["liked"]==1 else -1.7 if r["liked"]==-1 else 0)+(0 if r["rating"] is None else (r["rating"]-5)*.45)
  for g in (r["genres"] or "").split("،"):out[g.strip()]=out.get(g.strip(),0)+val
 return out
def match(m,w):
 gs=[x.strip() for x in (m["genres"] or "").split("،")]
 return max(50,min(99,round(75+sum(w.get(g,0) for g in gs)/max(1,len(gs))*5)))
def tmdb(path,params=None):
 if not TOKEN:return None,"أضف TMDB_READ_TOKEN إلى متغيرات البيئة أولًا."
 try:
  r=requests.get("https://api.themoviedb.org/3/"+path,params=params or {},headers={"Authorization":"Bearer "+TOKEN,"accept":"application/json"},timeout=20);r.raise_for_status();return r.json(),None
 except Exception as e:return None,"تعذر الاتصال بـ TMDB: "+str(e)
def import_movies(items):
 c=db();n=0
 for x in items:
  tid=x.get("id");title=x.get("title") or x.get("original_title")
  if not tid or not title:continue
  y=(x.get("release_date") or "")[:4]
  c.execute("INSERT OR IGNORE INTO movies(title,year,country,genres,overview,tmdb_id,poster_path) VALUES(?,?,?,?,?,?,?)",(title,int(y) if y.isdigit() else None,"🌍 غير محدد","اكتشاف جديد",x.get("overview") or "لا يتوفر ملخص بعد.",tid,x.get("poster_path")))
  n+=c.execute("SELECT changes()").fetchone()[0]
 c.commit();c.close();return n
st.markdown("""<style>
.stApp{background:radial-gradient(ellipse at 80% 0%,#153e66,transparent 40%),#061426;color:#eef7ff}
section[data-testid="stSidebar"]{background:#07172b}
h1,h2,h3{color:#eff8ff}.eyebrow{color:#78dcff;letter-spacing:3px;font-size:12px}
.hero{padding:24px;border:1px solid #2b557a;border-radius:22px;background:linear-gradient(110deg,#143d66,#0a2039);margin:12px 0 20px}
.poster{height:240px;border-radius:12px;background:radial-gradient(circle at 70% 20%,#6de0e4aa,transparent 25%),radial-gradient(circle at 20% 60%,#f58a4f99,transparent 30%),repeating-linear-gradient(135deg,transparent 0 30px,#c8f1ff20 31px 32px),linear-gradient(145deg,#102244,#285879,#071526);display:flex;align-items:end;justify-content:center;padding:15px;color:white;text-align:center;font-family:Georgia,serif;font-size:22px;font-weight:bold;text-shadow:0 2px 10px black;margin-bottom:8px}
div[data-testid="stVerticalBlockBorderWrapper"]{border-color:#24486d!important}
.small{color:#9db5d0;font-size:12px}
</style>""",unsafe_allow_html=True)
if "flash" not in st.session_state:st.session_state.flash=""
c=db()
with st.sidebar:
 st.markdown("# Cine<span style='color:#58c7ff'>Match</span> ✦",unsafe_allow_html=True)
 st.caption("اكتشف الفيلم اللي على مزاجك")
 page=st.radio("التنقل",["المكتبة الرئيسية","قائمة المشاهدة","شاهدتها","المفضلة","اكتشف أفلامًا","الإعدادات والمزامنة"])
 st.divider();st.caption("حفظ محلي · تحديثات اختيارية")
if st.session_state.flash:st.info(st.session_state.flash);st.session_state.flash=""
st.markdown('<div class="eyebrow">YOUR PERSONAL CINEMA</div>',unsafe_allow_html=True)
if page=="الإعدادات والمزامنة":
 st.title("إعدادات CineMatch")
 total=c.execute("SELECT COUNT(*) FROM movies").fetchone()[0]; synced=c.execute("SELECT COUNT(*) FROM movies WHERE tmdb_id IS NOT NULL").fetchone()[0]
 st.metric("أفلام المكتبة",total);st.metric("مستوردة من TMDB",synced)
 st.warning("حالة TMDB: "+("مفتاح API موجود" if TOKEN else "غير متصل — أضف TMDB_READ_TOKEN لتفعيل المزامنة"))
 st.markdown("### مزامنة أفلام مشهورة")
 pages=st.selectbox("حجم الدفعة",["20 فيلمًا تقريبًا","100 فيلم تقريبًا","200 فيلم تقريبًا","400 فيلم تقريبًا"],index=1)
 if st.button("مزامنة الأفلام الشعبية",type="primary"):
  n=0;err=None
  for p in range(1,{"20 فيلمًا تقريبًا":1,"100 فيلم تقريبًا":5,"200 فيلم تقريبًا":10,"400 فيلم تقريبًا":20}[pages]+1):
   data,e=tmdb("movie/popular",{"language":"en-US","page":p})
   if e:err=e;break
   n+=import_movies(data.get("results",[]))
  st.success(f"أضيف {n} فيلمًا جديدًا.") if not err else st.error(err)
 with st.form("search_tmdb"):
  query=st.text_input("ابحث عن فيلم محدد بالإنجليزية")
  if st.form_submit_button("بحث ومزامنة"):
   data,e=tmdb("search/movie",{"query":query,"include_adult":"false","language":"en-US","page":1}) if query else (None,"اكتب اسم الفيلم أولًا.")
   if e:st.error(e)
   else:st.success(f"أضيف {import_movies(data.get('results',[]))} فيلمًا جديدًا.")
 st.markdown("### المصادر والحقوق")
 st.markdown("- [توثيق TMDB API](https://developer.themoviedb.org/docs/getting-started)\n- [أساسيات صور TMDB](https://developer.themoviedb.org/docs/image-basics)\n- [شروط استخدام بيانات IMDb](https://help.imdb.com/article/imdb/general-information/can-i-use-imdb-data-in-my-software/G5JTRESSHJBBHTGX)")
 st.info("التقييمات الأولية قيم مرجعية تقريبية وليست تقييمات IMDb حية. لا يقوم البرنامج بكشط IMDb. بيانات البلد والتصنيفات للأفلام المستوردة تحتاج إثراءً إضافيًا.")
 st.caption('إسناد TMDB: “This product uses the TMDB API but is not endorsed or certified by TMDB.”')
elif page=="اكتشف أفلامًا":
 st.title("اكتشف فيلمك التالي")
 st.markdown('<div class="hero"><h2>جرّب سينما من مكان جديد.</h2><p>كل إعجاب أو رفض أو تقييم يغيّر أوزان الأنواع في الترشيحات القادمة.</p></div>',unsafe_allow_html=True)
 st.info("نسبة التوافق مؤشر تجريبي وليست احتمالًا علميًا للإعجاب.")
elif page in ["قائمة المشاهدة","شاهدتها","المفضلة"]:
 status={"قائمة المشاهدة":"watchlist","شاهدتها":"watched","المفضلة":"favorite"}[page]
 st.title(page)
 rows=c.execute("SELECT m.*,f.liked,f.rating,f.status FROM movies m JOIN feedback f ON m.id=f.movie_id WHERE f.status=? ORDER BY m.title",(status,)).fetchall()
 if not rows:st.info("القائمة فارغة حاليًا. أضف فيلمًا من المكتبة الرئيسية.")
else:
 st.title("مكتبتك السينمائية")
 st.markdown('<div class="hero"><div class="eyebrow">CURATED WORLD CINEMA</div><h2>مش مجرد فيلم… دي الحكاية اللي جاية على ذوقك.</h2><p>بوسترات فنية بديلة، سينما عالمية، وتوصيات تتطور من تقييماتك.</p></div>',unsafe_allow_html=True)
 q=st.text_input("ابحث عن فيلم أو فكرة أو نوع")
 allrows=c.execute("SELECT * FROM movies").fetchall()
 genres=sorted(set(g.strip() for m in allrows for g in (m["genres"] or "").split("،")))
 countries=sorted(set(m["country"] for m in allrows if m["country"]))
 col1,col2=st.columns(2)
 with col1:genre=st.selectbox("التصنيف",["الكل"]+genres)
 with col2:country=st.selectbox("بلد الفيلم",["الكل"]+countries)
 rows=[m for m in allrows if (not q or q.lower() in (m["title"]+" "+m["overview"]+" "+m["genres"]+" "+m["country"]).lower()) and (genre=="الكل" or genre in m["genres"]) and (country=="الكل" or country==m["country"])]
 st.caption(f"{len(rows)} نتيجة · {len(allrows)} فيلم في المكتبة")
w=weights(c)
if page not in ["الإعدادات والمزامنة","اكتشف أفلامًا"]:
 fbmap={r["movie_id"]:dict(r) for r in c.execute("SELECT * FROM feedback")}
 rows=sorted(rows,key=lambda m:(match(m,w),m["ref_rating"] or 0),reverse=True)
 for start in range(0,len(rows),4):
  cols=st.columns(4)
  for col,m in zip(cols,rows[start:start+4]):
   f=fbmap.get(m["id"],{})
   with col:
    poster="https://image.tmdb.org/t/p/w342"+m["poster_path"] if m["poster_path"] else ""
    if poster:
     st.image(poster,use_container_width=True)
    else:
     st.markdown(f'<div class="poster">{m["title"]}</div>',unsafe_allow_html=True)
    st.markdown("**"+m["title"]+"**")
    st.caption(f'{m["country"]} · {m["year"] or "—"}')
    st.markdown(f'⭐ **{m["ref_rating"]:.1f}/10** · مرجعي' if m["ref_rating"] else "⭐ التقييم غير متاح")
    st.caption(m["genres"])
    with st.expander("القصة والتفاصيل"):
     st.write(m["overview"])
     st.warning("تنبيهات المحتوى التفصيلية غير متاحة لهذه النسخة؛ لا تفترض أن الفيلم خالٍ من المحتوى الحساس.")
     if m["imdb_id"]:st.link_button("فتح IMDb",f'https://www.imdb.com/title/{m["imdb_id"]}/')
     with st.form(f'rate{m["id"]}'):
      val=st.slider("تقييمك الشخصي",1,10,value=int(f.get("rating") or 7))
      notes=st.text_input("ملاحظات أو تنبيهات محتوى",value=f.get("notes") or "")
      if st.form_submit_button("حفظ التقييم والملاحظات"):
       c.execute("INSERT INTO feedback(movie_id,rating,notes) VALUES(?,?,?) ON CONFLICT(movie_id) DO UPDATE SET rating=excluded.rating,notes=excluded.notes",(m["id"],val,notes));c.commit();st.session_state.flash="تم حفظ تقييمك وملاحظاتك.";st.rerun()
    a,b=st.columns(2)
    with a:
     if st.button("♡ إعجاب",key=f'like{m["id"]}'):
      c.execute("INSERT INTO feedback(movie_id,liked) VALUES(?,1) ON CONFLICT(movie_id) DO UPDATE SET liked=CASE WHEN liked=1 THEN 0 ELSE 1 END",(m["id"],));c.commit();st.session_state.flash="تم تسجيل تفضيلك.";st.rerun()
     if st.button("＋ لاحقًا",key=f'watch{m["id"]}'):
      c.execute("INSERT INTO feedback(movie_id,status) VALUES(?,'watchlist') ON CONFLICT(movie_id) DO UPDATE SET status=CASE WHEN status='watchlist' THEN '' ELSE 'watchlist' END",(m["id"],));c.commit();st.session_state.flash="تم تحديث قائمة المشاهدة.";st.rerun()
    with b:
     if st.button("👎 لا يعجبني",key=f'dislike{m["id"]}'):
      c.execute("INSERT INTO feedback(movie_id,liked) VALUES(?,-1) ON CONFLICT(movie_id) DO UPDATE SET liked=CASE WHEN liked=-1 THEN 0 ELSE -1 END",(m["id"],));c.commit();st.session_state.flash="سنتعلم من اختيارك.";st.rerun()
     if st.button("✓ شاهدته",key=f'seen{m["id"]}'):
      c.execute("INSERT INTO feedback(movie_id,status) VALUES(?,'watched') ON CONFLICT(movie_id) DO UPDATE SET status='watched'",(m["id"],));c.commit();st.session_state.flash="تم تسجيل الفيلم كمشاهد.";st.rerun()
 c.close()
 st.divider()
 st.caption("CineMatch Starter · واجهة تجريبية قابلة للتطوير. البوسترات البديلة التجريدية تُرسم داخل الواجهة، وليست لوحات فنية أصلية مرسومة لكل فيلم.")
