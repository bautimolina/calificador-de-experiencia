
const int SWITCH = 2;
const int LED_VERDE = 8;

const unsigned long REBOTE = 40;

int lecturaAnterior;
int estadoSwitch;

unsigned long ultimoCambio = 0;

bool encuestaActiva = false;
bool esperarApagado = false;

String comando = "";

void setup() {

  pinMode(SWITCH, INPUT_PULLUP);
  pinMode(LED_VERDE, OUTPUT);

  digitalWrite(LED_VERDE, LOW);

  Serial.begin(9600);

  lecturaAnterior = digitalRead(SWITCH);
  estadoSwitch = lecturaAnterior;

  if (estadoSwitch == LOW) {
    esperarApagado = true;
  }
}

void loop() {

  while (Serial.available() > 0) {

    char caracter = Serial.read();

    if (caracter == '\n') {

      comando.trim();

      if (comando == "FIN" && encuestaActiva) {

        encuestaActiva = false;

        digitalWrite(LED_VERDE, LOW);

        esperarApagado = (estadoSwitch == LOW);
      }

      comando = "";

    } else if (caracter != '\r') {

      comando += caracter;
    }
  }

  int lectura = digitalRead(SWITCH);

  if (lectura != lecturaAnterior) {

    lecturaAnterior = lectura;
    ultimoCambio = millis();
  }

  if (millis() - ultimoCambio >= REBOTE) {

    if (lectura != estadoSwitch) {

      estadoSwitch = lectura;

      if (estadoSwitch == HIGH) {

        esperarApagado = false;

      } else if (
        estadoSwitch == LOW &&
        !encuestaActiva &&
        !esperarApagado
      ) {

        encuestaActiva = true;

        digitalWrite(LED_VERDE, HIGH);

        Serial.println("INICIO");
      }
    }
  }
}
