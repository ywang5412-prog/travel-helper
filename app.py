from flask import Flask, render_template, request
import random

app = Flask(__name__)

# ==================== 資料庫模擬 (期末報告用展示資料) ====================
FOOD_DATA = {
    "台北": ["林東芳牛肉麵", "鼎泰豐", "寧夏夜市雞肉飯", "馬辣頂級麻辣鴛鴦火鍋"],
    "台中": ["屋馬燒肉", "逢甲夜市地瓜球", "宮原眼科冰淇淋", "輕井澤鍋物"],
    "高雄": ["丹丹漢堡", "六合夜市海產粥", "瑞豐夜市天使雞排", "碳佐麻里"]
}

ATTRACTIONS = {
    "台北": ["台北101", "故宮博物院", "西門町", "陽明山"],
    "台中": ["高美濕地", "勤美誠品綠園道", "審計新村", "逢甲夜市"],
    "高雄": ["駁二藝術特區", "西子灣", "旗津老街", "愛河"]
}

# ==================== 路由與功能邏輯 ====================

# 1. 首頁
@app.route('/')
def index():
    return render_template('index.html')

# 2. 美食推薦系統
@app.route('/food', methods=['GET', 'POST'])
def food():
    recommendations = []
    selected_city = None
    if request.method == 'POST':
        selected_city = request.form.get('city')
        if selected_city in FOOD_DATA:
            # 隨機推薦 2 個美食
            recommendations = random.sample(FOOD_DATA[selected_city], 2)
    return render_template('food.html', city=selected_city, foods=recommendations)

# 3. 旅遊行程規劃網站
@app.route('/travel', methods=['GET', 'POST'])
def travel():
    itinerary = []
    selected_city = None
    days = 1
    if request.method == 'POST':
        selected_city = request.form.get('city')
        days = int(request.form.get('days', 1))
        
        if selected_city in ATTRACTIONS:
            city_spots = ATTRACTIONS[selected_city]
            # 根據天數簡單規劃行程（每天排2個景點）
            for i in range(days):
                spots = random.sample(city_spots, min(2, len(city_spots)))
                itinerary.append({"day": i + 1, "spots": spots})
                
    return render_template('travel.html', city=selected_city, days=days, itinerary=itinerary)

# 4. 天氣預報與交通推薦網站
@app.route('/weather', methods=['GET', 'POST'])
def weather():
    weather_info = None
    transport_info = None
    selected_city = None
    
    if request.method == 'POST':
        selected_city = request.form.get('city')
        # 這裡使用模擬數據，若期末想拿高分，可自行串接中央氣象署 API
        weather_info = "☀️ 晴天，28°C ~ 32°C。天氣炎熱，請注意防曬與補充水分。"
        
        # 根據城市給予交通建議
        if selected_city == "台北":
            transport_info = "捷運非常便利，搭配 YouBike 即可輕鬆抵達各大景點。"
        elif selected_city == "台中":
            transport_info = "建議搭乘台中捷運或公車（可享優待），部分遠處景點建議租車。"
        else:
            transport_info = "可搭乘高雄捷運與輕軌，西子灣與旗津一帶建議步行或騎雙輪工具。"
            
    return render_template('weather.html', city=selected_city, weather=weather_info, transport=transport_info)

if __name__ == '__main__':
    # 這裡的 port 邏輯是為了配合 Render 的環境變數
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
