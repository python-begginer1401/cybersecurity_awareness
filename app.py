import streamlit as st
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="Cybersecurity Awareness Platform",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'language' not in st.session_state:
    st.session_state.language = "English"
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0

# Translation dictionaries
TEXTS = {
    "English": {
        "title": "Cybersecurity Awareness Platform",
        "sidebar_title": "🔒 Cybersecurity Awareness",
        "language_label": "🌐 Language",
        "api_section": "🔑 API Configuration",
        "api_placeholder": "Enter your Gemini API key",
        "api_success": "✓ API Key configured",
        "navigation": "🧭 Navigation",
        "progress": "📊 Your Progress",
        "footer": "Stay secure. Stay informed.",
        "home_title": "Cybersecurity Awareness Platform",
        "home_subtitle": "Complete Digital Protection Platform",
        "feature1_title": "🤖 AI Security Assistant",
        "feature1_desc": "Get instant answers to your cybersecurity questions from our AI expert",
        "feature2_title": "🔗 URL Threat Scanner", 
        "feature2_desc": "Analyze websites for potential security risks before visiting",
        "feature3_title": "📝 Security Assessment",
        "feature3_desc": "Test your knowledge with interactive quizzes and get feedback",
        "feature4_title": "📚 Learning Resources",
        "feature4_desc": "Access comprehensive guides and best practices",
        "chat_title": "🤖 AI Security Assistant",
        "chat_placeholder": "Ask about cybersecurity...",
        "chat_clear": "Clear Chat",
        "chat_thinking": "Analyzing your question...",
        "chat_error": "Failed to get response. Please check your API key.",
        "scanner_title": "🔗 URL Security Scanner",
        "scanner_placeholder": "Enter URL to scan...",
        "scanner_button": "🔍 Scan URL Security",
        "scanner_analyzing": "🔎 Analyzing URL for security threats...",
        "scanner_success": "✅ Security Analysis Complete",
        "scanner_report": "Security Report",
        "scanner_error": "❌ Analysis failed. Please check your API key.",
        "scanner_warning": "⚠️ Please enter a URL to scan",
        "quiz_title": "📝 Cybersecurity Knowledge Assessment",
        "quiz_submit": "Submit Answer",
        "quiz_retake": "Retake Assessment",
        "quiz_complete": "🎉 Assessment Complete! Score: {score}/3",
        "quiz_perfect": "**Perfect!** You have excellent cybersecurity knowledge!",
        "quiz_good": "**Good job!** You have solid cybersecurity awareness.",
        "quiz_improve": "**Keep learning!** Review the learning center to improve your knowledge.",
        "learn_title": "📚 Cybersecurity Learning Center",
        "password_title": "🔐 Password Security Best Practices",
        "email_title": "📧 Email Security & Phishing Protection",
        "browsing_title": "🌐 Safe Web Browsing Habits",
        "general_title": "🛡️ General Security Tips"
    },
    "Arabic": {
        "title": "منصة التوعية بالأمن السيبراني",
        "sidebar_title": "🔒 منصة الأمن السيبراني",
        "language_label": "🌐 اللغة",
        "api_section": "🔑 إعدادات API",
        "api_placeholder": "أدخل مفتاح Gemini API",
        "api_success": "✓ تم تكوين مفتاح API",
        "navigation": "🧭 التنقل",
        "progress": "📊 تقدمك",
        "footer": "ابق آمناً. ابق مطلعاً.",
        "home_title": "منصة التوعية بالأمن السيبراني",
        "home_subtitle": "منصة حماية رقمية شاملة",
        "feature1_title": "🤖 المساعد الأمني بالذكاء الاصطناعي",
        "feature1_desc": "احصل على إجابات فورية لأسئلتك الأمنية من خبيرنا بالذكاء الاصطناعي",
        "feature2_title": "🔗 ماسح تهديدات الروابط",
        "feature2_desc": "حلل المواقع بحثاً عن مخاطر أمنية محتملة قبل زيارتها",
        "feature3_title": "📝 التقييم الأمني",
        "feature3_desc": "اختبر معرفتك باختبارات تفاعلية واحصل على ملاحظات",
        "feature4_title": "📚 المصادر التعليمية", 
        "feature4_desc": "الوصول إلى أدلة شاملة وأفضل الممارسات",
        "chat_title": "🤖 المساعد الأمني الذكي",
        "chat_placeholder": "اسأل عن الأمن السيبراني...",
        "chat_clear": "مسح المحادثة",
        "chat_thinking": "جاري تحليل سؤالك...",
        "chat_error": "فشل في الحصول على الرد. يرجى التحقق من مفتاح API.",
        "scanner_title": "🔗 ماسح أمان الروابط",
        "scanner_placeholder": "أدخل الرابط للمسح...",
        "scanner_button": "🔍 مسح أمان الرابط",
        "scanner_analyzing": "🔎 جاري تحليل الرابط للكشف عن التهديدات...",
        "scanner_success": "✅ اكتمل التحليل الأمني",
        "scanner_report": "التقرير الأمني",
        "scanner_error": "❌ فشل التحليل. يرجى التحقق من مفتاح API.",
        "scanner_warning": "⚠️ الرجاء إدخال رابط للمسح",
        "quiz_title": "📝 اختبار المعرفة بالأمن السيبراني",
        "quiz_submit": "إرسال الإجابة",
        "quiz_retake": "أعد التقييم",
        "quiz_complete": "🎉 اكتمل التقييم! النتيجة: {score}/3",
        "quiz_perfect": "**ممتاز!** لديك معرفة ممتازة بالأمن السيبراني!",
        "quiz_good": "**عمل جيد!** لديك وعي قوي بالأمن السيبراني.",
        "quiz_improve": "**استمر في التعلم!** راجع مركز التعلم لتحسين معرفتك.",
        "learn_title": "📚 مركز التعلم بالأمن السيبراني",
        "password_title": "🔐 أفضل ممارسات أمان كلمات المرور",
        "email_title": "📧 أمان البريد الإلكتروني والحماية من التصيد",
        "browsing_title": "🌐 عادات التصفح الآمن للويب",
        "general_title": "🛡️ نصائح أمنية عامة"
    }
}

def get_text(key):
    """Get text in current language"""
    return TEXTS[st.session_state.language].get(key, key)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with clean navigation
with st.sidebar:
    st.markdown(f'<div class="sidebar-header">{get_text("sidebar_title")}</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Language Selector
    st.markdown(f"**{get_text('language_label')}**")
    language = st.selectbox(
        "Choose language:",
        ["English", "Arabic"],
        label_visibility="collapsed",
        key="language_selector"
    )
    
    if language != st.session_state.language:
        st.session_state.language = language
        st.session_state.chat_history = []
        st.session_state.quiz_score = 0
        st.session_state.current_question = 0
        st.rerun()
    
    st.markdown("---")
    
    # API Key Section
    st.markdown(f"**{get_text('api_section')}**")
    api_key = st.text_input("API Key", type="password", label_visibility="collapsed", placeholder=get_text("api_placeholder"))
    if api_key:
        st.session_state.api_key = api_key
        st.success(get_text("api_success"))
    
    st.markdown("---")
    
    # Navigation Section
    st.markdown(f"**{get_text('navigation')}**")
    
    # Create navigation options
    if st.session_state.language == "English":
        nav_options = ["🏠 Home", "🤖 AI Assistant", "🔗 URL Scanner", "📝 Security Quiz", "📚 Learning Center"]
    else:
        nav_options = ["🏠 الرئيسية", "🤖 المساعد الذكي", "🔗 ماسح الروابط", "📝 اختبار الأمن", "📚 مركز التعلم"]
    
    selected_page = st.radio(
        "Choose a section:",
        nav_options,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown(f"**{get_text('progress')}**")
    st.metric("Quiz Score" if st.session_state.language == "English" else "النتيجة", f"{st.session_state.quiz_score}/3")
    
    st.markdown("---")
    st.caption(get_text("footer"))

# Get the actual page name from the selected radio option
page_map = {
    "English": {
        "🏠 Home": "home",
        "🤖 AI Assistant": "chat", 
        "🔗 URL Scanner": "scanner",
        "📝 Security Quiz": "quiz",
        "📚 Learning Center": "learn"
    },
    "Arabic": {
        "🏠 الرئيسية": "home",
        "🤖 المساعد الذكي": "chat", 
        "🔗 ماسح الروابط": "scanner",
        "📝 اختبار الأمن": "quiz",
        "📚 مركز التعلم": "learn"
    }
}

current_page = page_map[st.session_state.language][selected_page]

# Home Page
if current_page == "home":
    st.markdown(f'<div class="main-header">{get_text("home_title")}</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="feature-card">
        <h3>🛡️ {get_text("home_subtitle")}</h3>
        <p>{"Learn, practice, and implement cybersecurity best practices to protect your digital life from modern threats." if st.session_state.language == "English" else "تعلم ومارس ونفذ أفضل ممارسات الأمن السيبراني لحماية حياتك الرقمية من التهديدات الحديثة."}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Grid
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### {get_text('feature1_title')}")
        st.markdown(get_text("feature1_desc"))
        
        st.markdown(f"### {get_text('feature2_title')}")
        st.markdown(get_text("feature2_desc"))
    
    with col2:
        st.markdown(f"### {get_text('feature3_title')}")
        st.markdown(get_text("feature3_desc"))
        
        st.markdown(f"### {get_text('feature4_title')}")
        st.markdown(get_text("feature4_desc"))
# AI Assistant Page
elif current_page == "chat":
    st.markdown(f'<div class="main-header">{get_text("chat_title")}</div>', unsafe_allow_html=True)
    
    if 'api_key' not in st.session_state:
        st.warning("🔑 " + ("Please enter your Gemini API key in the sidebar" if st.session_state.language == "English" else "الرجاء إدخال مفتاح API في الشريط الجانبي"))
    else:
        # Initialize processing state
        if 'processing' not in st.session_state:
            st.session_state.processing = False
        if 'last_processed_prompt' not in st.session_state:
            st.session_state.last_processed_prompt = ""
        
        # Display chat history
        if st.session_state.chat_history:
            st.markdown("💬 " + ("Conversation" if st.session_state.language == "English" else "المحادثة"))
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f"**{'You' if st.session_state.language == 'English' else 'أنت'}:** {msg['content']}")
                else:
                    st.markdown(f"**{'Assistant' if st.session_state.language == 'English' else 'المساعد'}:** {msg['content']}")
                st.markdown("---")
        
        # Chat input - only process if not currently processing and prompt is new
        prompt = st.chat_input(get_text("chat_placeholder"), disabled=st.session_state.processing)
        
        if prompt and not st.session_state.processing and prompt != st.session_state.last_processed_prompt:
            st.session_state.processing = True
            st.session_state.last_processed_prompt = prompt
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            # Use a placeholder to show the processing state
            processing_placeholder = st.empty()
            with processing_placeholder:
                with st.spinner(get_text("chat_thinking")):
                    try:
                        genai.configure(api_key=st.session_state.api_key)
                        model = genai.GenerativeModel("gemini-2.0-flash")
                        
                        if st.session_state.language == "English":
                            response_text = model.generate_content(f"""
                            As a cybersecurity expert, provide clear, practical advice for this question in English:
                            
                            {prompt}
                            
                            Focus on actionable steps and best practices. Keep response under 200 words.
                            """).text
                        else:
                            response_text = model.generate_content(f"""
                            كخبير في الأمن السيبراني، قدم نصائح عملية وواضحة لهذا السؤال بالعربية:
                            
                            {prompt}
                            
                            ركز على الخطوات القابلة للتطبيق وأفضل الممارسات. أجب بأقل من 100 كلمة.
                            """).text
                        
                        st.session_state.chat_history.append({"role": "assistant", "content": response_text})
                        
                    except Exception as e:
                        st.error(get_text("chat_error"))
                    finally:
                        # Clear the processing state and placeholder
                        processing_placeholder.empty()
                        st.session_state.processing = False
                        # Force a rerun to show the updated chat
                        st.rerun()
        
        # Clear chat button
        if st.session_state.chat_history:
            if st.button(get_text("chat_clear"), use_container_width=True, disabled=st.session_state.processing):
                st.session_state.chat_history = []
                st.session_state.last_processed_prompt = ""
                st.rerun()
# URL Scanner Page
elif current_page == "scanner":
    st.markdown(f'<div class="main-header">{get_text("scanner_title")}</div>', unsafe_allow_html=True)
    
    if 'api_key' not in st.session_state:
        st.warning("🔑 " + ("Please enter your Gemini API key in the sidebar" if st.session_state.language == "English" else "الرجاء إدخال مفتاح API في الشريط الجانبي"))
    else:
        url = st.text_input(
            "Enter URL to scan:" if st.session_state.language == "English" else "أدخل الرابط للمسح:", 
            placeholder="https://example.com"
        )
        
        if st.button(get_text("scanner_button"), use_container_width=True, type="primary"):
            if url:
                with st.spinner(get_text("scanner_analyzing")):
                    try:
                        genai.configure(api_key=st.session_state.api_key)
                        model = genai.GenerativeModel("gemini-2.0-flash")
                        
                        if st.session_state.language == "English":
                            response_text = model.generate_content(f"""
                            Briefly check if this URL is safe: {url}. Answer in 2-3 sentences.
                            """).text
                        else:
                            response_text = model.generate_content(f"""
                            "تحقق باختصار مما إذا كان هذا الرابط آمناً: {url}. أجب في 2-3 جمل."
                            """).text
                        
                        st.success(get_text("scanner_success"))
                        st.markdown(f"### {get_text('scanner_report')}")
                        st.info(response_text)
                        
                    except Exception as e:
                        st.error(get_text("scanner_error"))
            else:
                st.warning(get_text("scanner_warning"))

# Security Quiz Page
elif current_page == "quiz":
    st.markdown(f'<div class="main-header">{get_text("quiz_title")}</div>', unsafe_allow_html=True)
    
    # Quiz questions
    questions = {
        "English": [
            {
                "question": "What's the most secure approach to password management?",
                "options": [
                    "Use the same strong password everywhere",
                    "Write down passwords in a notebook",
                    "Use a password manager with unique passwords",
                    "Use simple passwords you can remember"
                ],
                "correct": 2
            },
            {
                "question": "How can you identify a phishing email?",
                "options": [
                    "It has perfect grammar and spelling",
                    "It comes from an unknown sender with urgent requests",
                    "It uses your full official name",
                    "It has no links or attachments"
                ],
                "correct": 1
            },
            {
                "question": "Why is two-factor authentication important?",
                "options": [
                    "It makes logging in faster",
                    "It adds an extra layer of security beyond passwords",
                    "It reduces internet costs",
                    "It's only for banking websites"
                ],
                "correct": 1
            }
        ],
        "Arabic": [
            {
                "question": "ما هي الطريقة الأكثر أماناً لإدارة كلمات المرور؟",
                "options": [
                    "استخدام نفس كلمة المرور القوية في كل مكان",
                    "كتابة كلمات المرور في دفتر ملاحظات",
                    "استخدام مدير كلمات مرور بكلمات مرور فريدة",
                    "استخدام كلمات مرور بسيطة يمكن تذكرها"
                ],
                "correct": 2
            },
            {
                "question": "كيف يمكنك التعرف على بريد تصيد احتيالي؟",
                "options": [
                    "يكون ذو قواعد إملائية ونحوية مثالية",
                    "يأتي من مرسل مجهول مع طلبات عاجلة",
                    "يستخدم اسمك الرسمي الكامل",
                    "لا يحتوي على روابط أو مرفقات"
                ],
                "correct": 1
            },
            {
                "question": "لماذا تعتبر المصادقة الثنائية مهمة؟",
                "options": [
                    "تجعل تسجيل الدخول أسرع",
                    "تضيف طبقة أمان إضافية",
                    "تقلل تكاليف الإنترنت",
                    "هي فقط لمواقع البنوك"
                ],
                "correct": 1
            }
        ]
    }
    
    current_questions = questions[st.session_state.language]
    
    # Check if quiz is completed
    if st.session_state.current_question >= len(current_questions):
        st.balloons()
        st.success(get_text("quiz_complete").format(score=st.session_state.quiz_score))
        
        if st.session_state.quiz_score == len(current_questions):
            st.success(get_text("quiz_perfect"))
        elif st.session_state.quiz_score >= 2:
            st.warning(get_text("quiz_good"))
        else:
            st.info(get_text("quiz_improve"))
        
        if st.button(get_text("quiz_retake"), use_container_width=True):
            st.session_state.current_question = 0
            st.session_state.quiz_score = 0
            st.rerun()
    
    else:
        # Show current question
        q = current_questions[st.session_state.current_question]
        
        st.write(f"**{'Question' if st.session_state.language == 'English' else 'السؤال'} {st.session_state.current_question + 1} {'of' if st.session_state.language == 'English' else 'من'} {len(current_questions)}**")
        st.write(f"**{q['question']}**")
        
        # Use a unique key for each question to prevent state issues
        selected = st.radio(
            "Select your answer:" if st.session_state.language == "English" else "اختر إجابتك:", 
            q["options"],
            key=f"question_{st.session_state.current_question}"
        )
        
        if st.button(get_text("quiz_submit"), use_container_width=True, key=f"submit_{st.session_state.current_question}"):
            if q["options"].index(selected) == q["correct"]:
                st.session_state.quiz_score += 1
                st.success("✅ " + ("Correct! Well done." if st.session_state.language == "English" else "صحيح! أحسنت."))
            else:
                correct_answer = q["options"][q["correct"]]
                st.error(f"❌ {'Incorrect. The correct answer is:' if st.session_state.language == 'English' else 'غير صحيح. الإجابة الصحيحة هي:'} {correct_answer}")
            
            # Move to next question
            st.session_state.current_question += 1
            
            # Use a small delay before rerun to show the feedback
            import time
            time.sleep(1.5)
            st.rerun()

# Learning Center Page
elif current_page == "learn":
    st.markdown(f'<div class="main-header">{get_text("learn_title")}</div>', unsafe_allow_html=True)
    
    if st.session_state.language == "English":
        with st.expander(get_text("password_title"), expanded=True):
            st.markdown("""
            **Create Strong Passwords:**
            - Use at least 12 characters
            - Mix uppercase and lowercase letters
            - Include numbers and symbols
            - Avoid personal information
            - Don't use dictionary words
            
            **Password Management:**
            - Use a reputable password manager
            - Enable two-factor authentication
            - Never reuse passwords across sites
            - Change passwords after security breaches
            """)
        
        with st.expander(get_text("email_title")):
            st.markdown("""
            **Identify Phishing Attempts:**
            - Check sender email addresses carefully
            - Look for spelling and grammar errors
            - Be wary of urgent or threatening language
            - Hover over links to see actual URLs
            - Don't open unexpected attachments
            """)
        
        with st.expander(get_text("browsing_title")):
            st.markdown("""
            **Secure Browsing:**
            - Always look for HTTPS in URLs
            - Keep browsers and extensions updated
            - Use ad blockers and anti-tracking
            - Avoid public WiFi for sensitive activities
            - Clear cookies and cache regularly
            """)
        
        with st.expander(get_text("general_title")):
            st.markdown("""
            **Device Security:**
            - Keep operating systems updated
            - Install reputable antivirus software
            - Use firewalls
            - Backup data regularly
            
            **Online Behavior:**
            - Be cautious with social media sharing
            - Monitor financial statements
            - Stay informed about new threats
            """)
    else:
        with st.expander(get_text("password_title"), expanded=True):
            st.markdown("""
            **إنشاء كلمات مرور قوية:**
            - استخدم 12 حرفاً على الأقل
            - اخلط بين الأحرف الكبيرة والصغيرة
            - أضف أرقاماً ورموزاً
            - تجنب المعلومات الشخصية
            - لا تستخدم كلمات من القاموس
            
            **إدارة كلمات المرور:**
            - استخدم مدير كلمات مرور موثوقاً
            - فعّل المصادقة الثنائية
            - لا تعيد استخدام كلمات المرور عبر المواقع
            - غيّر كلمات المرور بعد الاختراقات الأمنية
            """)
        
        with st.expander(get_text("email_title")):
            st.markdown("""
            **تحديد محاولات التصيد:**
            - تحقق من عناوين بريد المرسلين بعناية
            - ابحث عن أخطاء إملائية ونحوية
            - كن حذراً من اللغة العاجلة أو التهديدية
            - مرر فوق الروابط لرؤية عناوين URL الفعلية
            - لا تفتح المرفقات غير المتوقعة
            """)
        
        with st.expander(get_text("browsing_title")):
            st.markdown("""
            **التصفح الآمن:**
            - ابحث دائماً عن HTTPS في عناوين URL
            - حافظ على تحديث المتصفحات والإضافات
            - استخدم مانعات الإعلانات ومضادات التتبع
            - تجنب الواي فاي العام للأنشطة الحساسة
            - امسح ملفات تعريف الارتباط بانتظام
            """)
        
        with st.expander(get_text("general_title")):
            st.markdown("""
            **أمان الأجهزة:**
            - حافظ على تحديث أنظمة التشغيل
            - ثبّت برامج مكافحة فيروسات موثوقة
            - استخدم جدران الحماية
            - احفظ نسخاً احتياطية من البيانات
            
            **السلوك عبر الإنترنت:**
            - كن حذراً مع المشاركة على وسائل التواصل
            - راقب كشوف الحسابات المالية
            - ابق مطلعاً على التهديدات الجديدة
            """)
