import time
import random
import uuid
import os
from datetime import datetime

# Konfigurace
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "logs", "api-gw", "privat.log"))
ENCODING = 'cp1250'
DELAY_SECONDS = (1.0, 3.0)  # Náhodná pauza mezi logy v sekundách

# Ukázkové moduly a zprávy pro věrnější simulaci
MODULES = ["Global@39", "Global@31", "Global@18", "BusinessLogicModule@20", "VopBdpApi@39", "MailDispatcherModule@43"]

def get_random_process_id():
    return uuid.uuid4().hex

def get_random_trace_id():
    return str(uuid.uuid4())

def generate_log_line(current_time):
    timestamp_str = current_time.strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
    
    # Výběr typu zprávy
    scenario = random.choices(["HEALTH", "ONBOARDING", "SYSTEM", "MAIL"], weights=[40, 40, 15, 5])[0]
    
    level = "INFO"
    log_id = str(random.randint(60000, 99999))
    module = random.choice(MODULES)
    
    if scenario == "HEALTH":
        trace_id = get_random_trace_id()
        msg_type = random.choices(["Started", "Finished"], weights=[50, 50])[0]
        
        # Občasné varování (5% šance) u hotového testu
        if msg_type == "Finished" and random.random() < 0.05:
            level = "WARN"
            message = f"Activity 'Health' Finished - SLOW RESPONSE {random.randint(500, 1500)} ms - traceId={trace_id}"
        elif msg_type == "Started":
            message = f"Activity 'Health' Started - traceId={trace_id}"
        else:
            message = f"Activity 'Health' Finished - {random.randint(10, 150)} ms - traceId={trace_id}"
    
    elif scenario == "ONBOARDING":
        process_id = get_random_process_id()
        step = random.choice(["PhoneVerification", "EmailVerification", "IdentifyClient", "VerifyIdentity"])
        op = random.choice(["ResendOtp", "SubmitEmailAddress", "VerifyPhoneNumberOtp", "VerifyIdentity"])
        
        rand = random.random()
        # Simulace chyby (5% šance)
        if rand < 0.05:
            level = "ERROR"
            message = f"Activity '{op}' Failed - Critical database connection error - process {process_id}"
        # Simulace varování (10% šance: 0.05 až 0.15)
        elif rand < 0.15:
            level = "WARN"
            reasons = ["Invalid input parameters", "Timeout waiting for external service", "User failed OTP verification", "High latency detected"]
            message = f"Activity '{op}' Warning - {random.choice(reasons)} - process {process_id}"
        # Simulace dokončení s latencí
        elif rand > 0.8:
            message = f"Activity '{op}' Finished - {random.randint(200, 2000)} ms - process {process_id}"
        elif rand > 0.6:
            message = f"Onboarding.{op}: process {process_id}"
        else:
            message = f"Onboarding.{op}: Onboarding step set to {step} in process {process_id}"

    elif scenario == "MAIL":
        email = f"user{random.randint(100, 999)}@example.com"
        if random.random() < 0.1:
            level = "WARN"
            message = f"E-mail na adresu {email} byl zařazen do fronty kvůli dočasné nedostupnosti serveru SMTP"
        else:
            message = f"Odeslán e-mail na adresu {email} ('Privatbanka: OTP pre dokoncenie registrácie je', 76 znaku)"

    else: # SYSTEM
        rand = random.random()
        if rand < 0.02:
            level = "ERROR"
            message = "Kritická chyba: Nepodařilo se navázat spojení se systémem Centris"
        elif rand < 0.12:
            level = "WARN"
            message = random.choice([
                "Využití systémové paměti překročilo 85 %",
                "Odezva z databáze OfficeLine je pomalejší než obvykle",
                "Některé asynchronní příkazy nebylo možné dokončit včas",
                "Zjistěno podezřelé množství neúspěšných přihlášení z jedné IP"
            ])
        else:
            level = random.choice(["DEBUG", "INFO"])
            msg = random.choice([
                "Proběhlo zpracování čekajících příkazů",
                "Zpracování čekajících příkazů doběhlo",
                "Modul se ukoncuje",
                "Inicializace modulu dokončena"
            ])
            message = msg

    # Formátování levelu a mezer (INFO + 5 mezer, DEBUG + 4 mezery)
    level_field = f"{level:<9}"
    
    return f"{timestamp_str} {level_field}{log_id} [{module}]  {message}"

def main():
    abs_log_path = os.path.abspath(LOG_FILE)
    print(f"Log generátor spuštěn. Zapisuji do: {abs_log_path}", flush=True)
    print("Stiskněte Ctrl+C pro ukončení.", flush=True)
    
    # Zajistíme, aby adresář existoval
    log_dir = os.path.dirname(abs_log_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    try:
        while True:
            log_line = generate_log_line(datetime.now())
            with open(abs_log_path, "a", encoding=ENCODING) as f:
                f.write(log_line + "\n")
            
            # Výpis do konzole pro vizuální kontrolu
            print(f"[OK] Vygenerován log: {log_line}", flush=True)
            
            time.sleep(random.uniform(*DELAY_SECONDS))
    except KeyboardInterrupt:
        print("\nGenerování zastaveno uživatelem.", flush=True)
    except Exception as e:
        print(f"\nCHYBA: {e}", flush=True)

if __name__ == "__main__":
    main()
