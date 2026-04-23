import time
import random
import uuid
import os
from datetime import datetime, timedelta

# Konfigurace
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "logs", "api-gw", "onboarding.log"))
ENCODING = 'cp1250'

# Moduly
MODULES = ["OnboardingModule@10", "IdentityService@15", "OtpService@22", "DocumentService@8", "CrmIntegration@42"]

# Definice kroků a jejich možných logů
STEPS_CONFIG = [
    {"id": "INTRO", "op": "Init", "messages": ["Onboarding step set to INTRO"]},
    {"id": "CONTACT_PHONE", "op": "PhoneVerification", "substeps": [
        {"id": "OTP_SENT", "messages": ["Onboarding step set to OTP_SENT"]},
        {"id": "OTP_VERIFIED", "messages": ["Onboarding step set to OTP_VERIFIED"]}
    ]},
    {"id": "CONTACT_EMAIL", "op": "EmailVerification", "substeps": [
        {"id": "OTP_SENT", "messages": ["Onboarding step set to OTP_SENT"]},
        {"id": "OTP_VERIFIED", "messages": ["Onboarding step set to OTP_VERIFIED"]}
    ]},
    {"id": "IDENTITY_CAPTURE", "op": "IdentifyClient", "substeps": [
        {"id": "ZENID_FINALIZE", "messages": ["Onboarding step set to ZENID_FINALIZE"]},
        {"id": "DATA_CONFIRMATION", "messages": ["Onboarding step set to DATA_CONFIRMATION"]}
    ]},
    {"id": "PEP", "op": "AmlCheck", "messages": ["Onboarding step set to PEP"]},
    {"id": "SOURCE_OF_WEALTH", "op": "AmlCheck", "messages": ["Onboarding step set to SOURCE_OF_WEALTH"]},
    {"id": "PURPOSE_RELATIONSHIP", "op": "AmlCheck", "messages": ["Onboarding step set to PURPOSE_RELATIONSHIP"]},
    {"id": "REGULATORY_DATA", "op": "AmlSubmit", "messages": ["Onboarding step set to REGULATORY_DATA"]},
    {"id": "DOCUMENTATION", "op": "ContractGeneration", "substeps": [
        {"id": "PREVIEW_DOWNLOAD", "messages": ["Onboarding step set to PREVIEW_DOWNLOAD"]}
    ]},
    {"id": "CONTRACT_SIGNATURE", "op": "SignContract", "messages": ["Onboarding step set to CONTRACT_SIGNATURE"]},
    {"id": "PRODUCT_SELECTION", "op": "ProductSelection", "messages": ["Onboarding step set to PRODUCT_SELECTION"]},
    {"id": "CREDENTIALS_SETUP", "op": "SecuritySetup", "messages": ["Onboarding step set to CREDENTIALS_SETUP"]},
    {"id": "PUSH_REGISTRATION", "op": "RegisterPush", "messages": ["Onboarding step set to PUSH_REGISTRATION"]},
    {"id": "ACTIVATION", "op": "MobileActivation", "messages": ["Onboarding step set to ACTIVATION"]},
    {"id": "STATUS_POLLING", "op": "GetStatus", "messages": ["Onboarding status check: READY_FOR_TOKEN_ACTIVATION"]},
    {"id": "COMPLETED", "op": "ActivateToken", "messages": ["Onboarding step set to COMPLETED"]}
]

SCENARIOS = {
    "happy_path": {
        "weight": 60,
        "max_step": len(STEPS_CONFIG),
        "error_chance": 0.01
    },
    "early_drop_off": {
        "weight": 15,
        "max_step": 4, # Skončí u emailu
        "error_chance": 0.05
    },
    "zenid_struggle": {
        "weight": 10,
        "max_step": 6,
        "error_chance": 0.3 # Zvýšena šance na chybu u ZenID
    },
    "slow_user": {
        "weight": 5,
        "max_step": len(STEPS_CONFIG),
        "error_chance": 0.01
    },
    "technical_error": {
        "weight": 5,
        "max_step": 10,
        "force_error_at_step": random.randint(1, 10),
        "error_chance": 1.0
    },
    "abandoned": {
        "weight": 5,
        "max_step": 2,
        "error_chance": 0.0
    }
}

EXTERNAL_SERVICES = ["ZenID", "AML_Registry", "SmsGateway", "CrmApi", "MailService"]

def flatten_metadata(d, prefix=""):
    items = []
    for k, v in d.items():
        new_key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            items.extend(flatten_metadata(v, new_key))
        else:
            items.append(f"{new_key}={v}")
    return items

class OnboardingSession:
    def __init__(self):
        self.process_id = f"ONB_{datetime.now().year}_{random.randint(100000, 999999)}"
        self.correlation_id = str(uuid.uuid4())
        self.scenario_name = random.choices(list(SCENARIOS.keys()), weights=[s["weight"] for s in SCENARIOS.values()])[0]
        self.scenario = SCENARIOS[self.scenario_name]
        self.current_step_idx = 0
        self.current_substep_idx = 0
        self.is_finished = False
        self.start_time = datetime.now()
        self.next_action_time = self.start_time + timedelta(seconds=random.uniform(1, 5))
        self.failed_attempts = 0
        self.retry_count = 0
        self.total_process_time = None
        
        # UX / Demografická data (pro dashboard 5)
        self.client_data = {
            "age_group": random.choice(["18-25", "26-35", "36-45", "46-60", "60+"]),
            "gender": random.choice(["MALE", "FEMALE"]),
            "nationality": random.choice(["CZE", "SVK", "DEU", "AUT"])
        }
        
        devices_config = [
            {"name": "iPhone 15 Pro", "os": "iOS"},
            {"name": "iPhone 14", "os": "iOS"},
            {"name": "Samsung S23", "os": "Android"},
            {"name": "Samsung A54", "os": "Android"},
            {"name": "Xiaomi 13", "os": "Android"},
            {"name": "Google Pixel 8", "os": "Android"}
        ]
        chosen_device = random.choice(devices_config)
        self.device = chosen_device["name"]
        self.ux_os = chosen_device["os"]
        
        self.ux_browser = "NativeApp"
        self.ux_app_version = random.choice(["2.3.0", "2.4.0", "2.4.1"])
        self.ux_language = random.choice(["cs", "cs", "sk", "en"])
        self.ux_resolution = random.choice(["390x844", "414x896", "360x800", "1080x2340"])
        
        self.last_step_time = self.start_time
        
        # KYC / ZenID data (pro dashboard 2)
        self.zenid_confidence = round(random.uniform(0.72, 0.99), 2)
        self.zenid_liveness = round(random.uniform(0.85, 1.0), 2)
        self.zenid_ocr_match = random.random() > 0.05
        self.zenid_doc_type = random.choice(["ID_CARD", "PASSPORT", "DRIVING_LICENSE"])
        self.zenid_expiry_days = random.randint(-10, 2000) # Simulujeme i expirované
        
        if self.zenid_confidence > 0.85 and self.zenid_liveness > 0.9 and self.zenid_ocr_match and self.zenid_expiry_days > 0:
            self.zenid_decision = "APPROVED"
            self.zenid_rejection_reason = None
        elif self.zenid_expiry_days <= 0:
            self.zenid_decision = "DENIED"
            self.zenid_rejection_reason = "EXPIRED_DOCUMENT"
        elif self.zenid_confidence < 0.80:
            self.zenid_decision = "DENIED"
            self.zenid_rejection_reason = "LOW_CONFIDENCE"
        elif not self.zenid_ocr_match:
            self.zenid_decision = "MANUAL_REVIEW"
            self.zenid_rejection_reason = "OCR_MISMATCH"
        else:
            self.zenid_decision = "MANUAL_REVIEW"
            self.zenid_rejection_reason = "POOR_LIGHTING"
        
        # AML data (pro dashboard 3)
        self.aml_risk = random.choices(["LOW", "MID", "HIGH"], weights=[80, 15, 5])[0]
        self.aml_pep = random.random() < 0.05
        self.aml_sanctions = "CLEAN" if random.random() > 0.02 else "HIT"
        self.aml_sanctions_type = random.choice(["PARTIAL_MATCH", "FULL_MATCH"]) if self.aml_sanctions == "HIT" else None
        self.aml_source_of_funds = random.choice(["EMPLOYMENT", "BUSINESS", "INVESTMENTS", "INHERITANCE", "SAVINGS"])
        self.aml_occupational_risk = random.choices(["LOW", "MEDIUM", "HIGH"], weights=[85, 12, 3])[0]
        
        # Rizikovost národnosti
        if self.client_data["nationality"] in ["CZE", "SVK"]:
            self.aml_nationality_risk = "LOW"
        elif self.client_data["nationality"] in ["DEU", "AUT"]:
            self.aml_nationality_risk = "MEDIUM"
        else:
            self.aml_nationality_risk = "HIGH"
        
        # UX data
        self.otp_attempts = {
            "CONTACT_PHONE": random.randint(1, 3) if random.random() < 0.2 else 1,
            "CONTACT_EMAIL": random.randint(1, 2) if random.random() < 0.1 else 1
        }

    def get_next_log(self):
        if self.is_finished:
            return None
        
        now = datetime.now()
        if now < self.next_action_time:
            return None

        # Kontrola, zda jsme už neměli skončit (Drop-off)
        if self.current_step_idx >= self.scenario["max_step"] or self.current_step_idx >= len(STEPS_CONFIG):
            last_step_id = STEPS_CONFIG[self.current_step_idx - 1]["id"] if self.current_step_idx > 0 else "NONE"
            if last_step_id != "COMPLETED":
                # Uživatel opustil proces předčasně
                self.is_finished = True
                metadata = {
                    "processId": self.process_id,
                    "correlationId": self.correlation_id,
                    "step": last_step_id,
                    "status": "ABANDONED",
                    "ux": {
                        "os": self.ux_os,
                        "browser": self.ux_browser,
                        "app_version": self.ux_app_version,
                        "language": self.ux_language,
                        "resolution": self.ux_resolution,
                        "exit_type": "USER_EXIT" if self.scenario_name != "technical_error" else "TIMEOUT",
                        "step_duration_sec": round((now - self.last_step_time).total_seconds(), 1)
                    }
                }
                message = f"Onboarding process ABANDONED after step {last_step_id} in process {self.process_id}"
                return self._format_log(now, "WARN", message, metadata)
            else:
                self.is_finished = True
                return None

        step_config = STEPS_CONFIG[self.current_step_idx]
        step_id = step_config["id"]
        op = step_config["op"]
        
        # Simulace chyby
        level = "INFO"
        message = ""
        metadata = {
            "step": step_id,
            "processId": self.process_id,
            "correlationId": self.correlation_id,
            "status": "STARTED"
        }
        
        # UX data
        metadata["ux"] = {
            "os": self.ux_os,
            "browser": self.ux_browser,
            "app_version": self.ux_app_version,
            "language": self.ux_language,
            "resolution": self.ux_resolution,
            "step_duration_sec": round((now - self.last_step_time).total_seconds(), 1)
        }
        self.last_step_time = now

        should_fail = random.random() < self.scenario["error_chance"]
        if "force_error_at_step" in self.scenario and self.scenario["force_error_at_step"] == self.current_step_idx:
            should_fail = True

        if should_fail and self.failed_attempts < 2:
            level = random.choice(["WARN", "ERROR"])
            reasons = [
                {"msg": "Timeout", "http": 504},
                {"msg": "Validation failed", "http": 400},
                {"msg": "External service unavailable", "http": 503},
                {"msg": "Network glitch", "http": 502},
                {"msg": "Unauthorized access", "http": 401}
            ]
            reason_data = random.choice(reasons)
            reason = reason_data["msg"]
            http_status = reason_data["http"]
            
            message = f"Activity '{op}' Failed - {reason} - process {self.process_id}"
            
            metadata["status"] = "FAILED"
            metadata["error_code"] = f"{op.upper()}_ERROR"
            metadata["error_detail"] = reason
            metadata["http_status"] = http_status
            metadata["retry_count"] = self.retry_count
            
            # Pokud jde o chybu externí služby, přidáme i název služby (pro Dashboard 4)
            if http_status in [502, 503, 504]:
                metadata["health"] = {
                    "service": random.choice(EXTERNAL_SERVICES),
                    "status": "DOWN"
                }
            
            self.failed_attempts += 1
            self.retry_count += 1
            # Zkusíme to znovu za chvíli
            self.next_action_time = now + timedelta(seconds=random.uniform(5, 15))
            return self._format_log(now, level, message, metadata)

        # Normální krok
        self.failed_attempts = 0
        metadata["status"] = "COMPLETED"
        if step_id == "STATUS_POLLING":
             metadata["status"] = "IN_PROGRESS"
             
        metadata["retry_count"] = self.retry_count
        self.retry_count = 0 # Reset po úspěchu
        
        # Doplnění specifických metadat pro dashboardy
        if step_id == "INTRO":
            metadata["client"] = self.client_data
            metadata["device"] = self.device
        
        elif step_id == "CONTACT_PHONE":
            metadata["substep"] = "OTP_VERIFIED" if self.current_substep_idx == 1 else "OTP_SENT"
            metadata["attemptsCount"] = self.otp_attempts["CONTACT_PHONE"]
        
        elif step_id == "CONTACT_EMAIL":
            metadata["substep"] = "OTP_VERIFIED" if self.current_substep_idx == 1 else "OTP_SENT"
            metadata["attemptsCount"] = self.otp_attempts["CONTACT_EMAIL"]

        elif step_id == "IDENTITY_CAPTURE":
            metadata["zenid"] = {
                "confidenceScore": self.zenid_confidence,
                "livenessScore": self.zenid_liveness,
                "ocrMatch": self.zenid_ocr_match,
                "documentType": self.zenid_doc_type,
                "expiryDays": self.zenid_expiry_days,
                "decision": self.zenid_decision
            }
            if self.zenid_rejection_reason:
                metadata["zenid"]["rejectionReason"] = self.zenid_rejection_reason
        
        elif step_id in ["PEP", "SOURCE_OF_WEALTH", "PURPOSE_RELATIONSHIP"]:
            metadata["aml"] = {
                "riskLevel": self.aml_risk,
                "pepStatus": self.aml_pep,
                "sanctionsCheck": self.aml_sanctions,
                "sanctionsType": self.aml_sanctions_type,
                "sourceOfFunds": self.aml_source_of_funds,
                "occupationalRisk": self.aml_occupational_risk,
                "nationalityRisk": self.aml_nationality_risk
            }
        
        elif step_id == "STATUS_POLLING":
            self.total_process_time = round((now - self.start_time).total_seconds(), 1)

        elif step_id == "COMPLETED":
            if self.total_process_time is None:
                self.total_process_time = round((now - self.start_time).total_seconds(), 1)

        # Trvání operace (pro dashboard 4)
        metadata["duration_ms"] = random.randint(50, 2500)

        if "substeps" in step_config:
            substep = step_config["substeps"][self.current_substep_idx]
            msg_text = random.choice(substep["messages"])
            message = f"Onboarding.{step_config['id']}: {msg_text} in process {self.process_id}"
            
            self.current_substep_idx += 1
            if self.current_substep_idx >= len(step_config["substeps"]):
                self.current_substep_idx = 0
                self.current_step_idx += 1
        else:
            msg_text = random.choice(step_config["messages"])
            message = f"Onboarding.{step_config['id']}: {msg_text} in process {self.process_id}"
            self.current_step_idx += 1

        # Delay pro další krok
        delay = random.uniform(2, 10)
        if self.scenario_name == "slow_user":
            delay = random.uniform(20, 60)
        self.next_action_time = now + timedelta(seconds=delay)
        
        return self._format_log(now, level, message, metadata)

    def _format_log(self, dt, level, message, metadata=None):
        timestamp_str = dt.strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
        log_id = str(random.randint(60000, 99999))
        module = random.choice(MODULES)
        level_field = f"{level:<9}"
        
        formatted_meta = ""
        if metadata:
            # Přidáme metadata jako prostý text na konec zprávy oddělený pipe
            meta_text = ", ".join(flatten_metadata(metadata))
            formatted_meta = f" | metadata={meta_text}"
            
        return f"{timestamp_str} {level_field}{log_id} [{module}]  {message}{formatted_meta}"

def generate_health_log(now):
    service = random.choice(EXTERNAL_SERVICES)
    status = "UP" if random.random() > 0.05 else "DOWN"
    level = "INFO" if status == "UP" else "ERROR"
    
    msg = f"Health check for service '{service}' returned {status}"
    metadata = {
        "health": {
            "service": service,
            "status": status,
            "response_time_ms": random.randint(10, 500) if status == "UP" else 0
        }
    }
    
    # Formátování jako u session (ale bez process_id apod.)
    dt = now
    timestamp_str = dt.strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
    log_id = str(random.randint(60000, 99999))
    module = "SystemMonitor@5"
    level_field = f"{level:<9}"
    
    meta_text = ", ".join(flatten_metadata(metadata))
    formatted_meta = f" | metadata={meta_text}"
    
    return f"{timestamp_str} {level_field}{log_id} [{module}]  {msg}{formatted_meta}"

def main():
    abs_log_path = os.path.abspath(LOG_FILE)
    print(f"Onboarding Log Generátor spuštěn.", flush=True)
    print(f"Zapisuji do: {abs_log_path}", flush=True)
    
    log_dir = os.path.dirname(abs_log_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    active_sessions = []
    
    try:
        while True:
            now = datetime.now()
            
            # Občas vygenerujeme samostatný health log (pro Dashboard 4)
            if random.random() < 0.05:
                health_log = generate_health_log(now)
                with open(abs_log_path, "a", encoding=ENCODING) as f:
                    f.write(health_log + "\n")
                print(f"[HEALTH] {health_log}", flush=True)

            # Možná vytvoříme novou session
            if len(active_sessions) < 5 and random.random() < 0.3:
                active_sessions.append(OnboardingSession())
            
            # Generujeme logy pro aktivní session
            for session in active_sessions[:]:
                log_line = session.get_next_log()
                if log_line:
                    with open(abs_log_path, "a", encoding=ENCODING) as f:
                        f.write(log_line + "\n")
                    print(f"[{session.scenario_name}] {log_line}", flush=True)
                
                if session.is_finished:
                    active_sessions.remove(session)
            
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nGenerování zastaveno.", flush=True)

if __name__ == "__main__":
    main()
