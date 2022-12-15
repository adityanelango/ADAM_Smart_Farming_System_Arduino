#include <SoftwareSerial.h>
//#include <Wire.h>
 
#define npk_RE 8
#define npk_DE 7
#define sph_RE 10
#define sph_DE 9
#define sph_power 13

const byte nitro[] = {0x01, 0x03, 0x00, 0x1e, 0x00, 0x01, 0xb5, 0xcc};
const byte phos[] = {0x01, 0x03, 0x00, 0x1f, 0x00, 0x01, 0xe4, 0x0c};
const byte pota[] = {0x01, 0x03, 0x00, 0x20, 0x00, 0x01, 0x85, 0xc0};
const byte sph[] = {0x01,0x03, 0x00, 0x06, 0x00, 0x01, 0x64, 0x0b};

byte npk_values[11];
byte sph_values[11];
SoftwareSerial npk_mod(2,3);
SoftwareSerial sph_mod(4,5);
 
void setup() {
  Serial.begin(9600);
  npk_mod.begin(9600);
  sph_mod.begin(9600);
  pinMode(npk_RE, OUTPUT);
  pinMode(npk_DE, OUTPUT);
  pinMode(sph_RE, OUTPUT);
  pinMode(sph_DE, OUTPUT);
  pinMode(sph_power, OUTPUT);
  digitalWrite(sph_power,HIGH);

 
  delay(3000);
}
 
void loop() {
  byte n,p,k,sph,npkval;
  n = nitrogen();
  delay(250);
  p = phosphorous();
  delay(250);
  k = potassium();
  delay(250);
  sph = soilph();
  delay(250);
  npkval = npkget();
  delay(250);
  
  Serial.print(n);
  Serial.print(p);
  Serial.print(k);
  Serial.println(sph);
  delay(2000);
}
 
byte nitrogen(){
  digitalWrite(npk_DE,HIGH);
  digitalWrite(npk_RE,HIGH);
  delay(10);
  if(npk_mod.write(nitro,sizeof(nitro))==8){
    digitalWrite(npk_DE,LOW);
    digitalWrite(npk_RE,LOW);
    for(byte i=0;i<7;i++){
    npk_values[i] = npk_mod.read();
    }
  }
  return npk_values[4];
}
 
byte phosphorous(){
  digitalWrite(npk_DE,HIGH);
  digitalWrite(npk_RE,HIGH);
  delay(10);
  if(npk_mod.write(phos,sizeof(phos))==8){
    digitalWrite(npk_DE,LOW);
    digitalWrite(npk_RE,LOW);
    for(byte i=0;i<7;i++){
    npk_values[i] = npk_mod.read();
    }
  }
  return npk_values[4];
}
 
byte potassium(){
  digitalWrite(npk_DE,HIGH);
  digitalWrite(npk_RE,HIGH);
  delay(10);
  if(npk_mod.write(pota,sizeof(pota))==8){
    digitalWrite(npk_DE,LOW);
    digitalWrite(npk_RE,LOW);
    for(byte i=0;i<7;i++){
    npk_values[i] = npk_mod.read();
    }
  }
  return npk_values[4];
}

byte soilph(){
  digitalWrite(sph_DE,HIGH);
  digitalWrite(sph_RE,HIGH);
  delay(10);
  if(sph_mod.write(sph,sizeof(sph))==8){
    digitalWrite(sph_DE,LOW);
    digitalWrite(sph_RE,LOW);
    for(byte i=0;i<7;i++){
    sph_values[i] = sph_mod.read();
    }
  }
  return sph_values[4];
}
