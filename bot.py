import time
import MetaTrader5 as mt5
import pandas as pd

# 1. الاتصال الآمن بمنصة MetaTrader 5
if not mt5.initialize():
    print("فشل الاتصال بمنصة MT5، تأكد من تفعيل Algo Trading")
    mt5.shutdown()
    quit()

symbol = "XAUUSD"
lot = 0.01
mt5.symbol_select(symbol, True)

def get_ict_fib_levels():
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H1, 0, 100)
    df = pd.DataFrame(rates)

    highest_high = df["high"].max()
    lowest_low = df["low"].min()
    price_range = highest_high - lowest_low

    levels = {
        "sweet_spot": lowest_low + (price_range * 0.705),
        "ote_end": lowest_low + (price_range * 0.79),
    }
    return levels, mt5.symbol_info_tick(symbol).ask

def send_buy_order(current_ask, sweet_spot):
    point = mt5.symbol_info(symbol).point
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": current_ask,
        "sl": sweet_spot - (100 * point),  # الستوب لوز تحت السويت سبوت بـ 100 نقطة
        "tp": current_ask + (200 * point),  # الهدف (أخذ الربح) فوق الدخول بـ 200 نقطة
        "deviation": 20,
        "magic": 234000,
        "comment": "ICT Automated Quant Order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILL_IOC,
    }

    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"فشل تنفيذ الصفقة، الكود: {result.retcode}")
    else:
        print(f"✅ تم فتح صفقة شراء للذهب بنجاح عند سعر: {current_ask}")

# حلقة المراقبة والتنفيذ المستمر
print("🏃 السكريبت يراقب مستويات الذهب حياً...")
try:
    while True:
        fibs, current_price = get_ict_fib_levels()

        # الشرط الخوارزمي: الدخول عند ملامسة منطقة الـ Sweet Spot بدقة داخل منطقة الخصم
        if current_price <= fibs["sweet_spot"] and current_price >= fibs["ote_end"]:
            print(f"🎯 السعر في منطقة الـ OTE! تنفيذ الشراء عند سعر: {current_price}")
            send_buy_order(current_price, fibs["sweet_spot"])
            break

        time.sleep(5)  # تحديث ومراجعة الأسعار كل 5 ثوانٍ
except KeyboardInterrupt:
    print("تم إيقاف المراقبة.")

mt5.shutdown()
