import{V as l}from"./VehicleConfig-281e945c.js";import{_ as p,u as a,k as m,l as f,G as r,E as t,y as i}from"./vendor-06e11d0e.js";import"./vendor-fortawesome-05d7e447.js";import"./index-3434d31b.js";import"./vendor-bootstrap-4263d7eb.js";import"./vendor-jquery-9fc083b4.js";import"./vendor-axios-22b906fb.js";import"./vendor-sortablejs-0bb60e5b.js";import"./dynamic-import-helper-be004503.js";const g={name:"VehicleSocPSACC",mixins:[l]},v={class:"vehicle-soc-psacc"};function c(n,e,b,_,C,h){const d=a("openwb-base-alert"),s=a("openwb-base-text-input"),u=a("openwb-base-number-input");return m(),f("div",v,[r(d,{subtype:"info"},{default:t(()=>e[3]||(e[3]=[i(' Der PSA Car Controller muss auf einem eigenen Host installiert werden, mit Zugangsdaten konfiguriert werden und dauerhaft laufen. Die openWB ruft den SoC zu Beginn der Ladung vom PSA Car Controller ab. Während der Ladung liefert PSA keine Updates. Daher wird der SoC während der Ladung aus dem Zählerstand berechnet. Ausschlaggebend für die Genauigkeit dieser Berechnung sind die beiden Einstellungen "Kapazität der Batterie" und "Wirkungsgrad der Ladeelektronik" im Fahrzeug-Profil. ')])),_:1}),r(s,{title:"IP oder Hostname",subtype:"host",required:"","model-value":n.vehicle.configuration.psacc_server_or_ip,"onUpdate:modelValue":e[0]||(e[0]=o=>n.updateConfiguration(o,"configuration.psacc_server_or_ip"))},{help:t(()=>e[4]||(e[4]=[i("Host, auf dem der PSA Car Controller läuft.")])),_:1},8,["model-value"]),r(u,{title:"Port",required:"",min:1,max:65535,"model-value":n.vehicle.configuration.psacc_port,"onUpdate:modelValue":e[1]||(e[1]=o=>n.updateConfiguration(o,"configuration.psacc_port"))},{help:t(()=>e[5]||(e[5]=[i("Nummer des Ports, den der PSA Car Controller verwendet.")])),_:1},8,["model-value"]),r(s,{title:"VIN",subtype:"text",required:"","model-value":n.vehicle.configuration.vehicle_vin,"onUpdate:modelValue":e[2]||(e[2]=o=>n.updateConfiguration(o,"configuration.vehicle_vin"))},{help:t(()=>e[6]||(e[6]=[i("Fahrzeug-Identifizierungsnummer des Fahrzeugs, von dem der SoC abgefragt wird.")])),_:1},8,["model-value"])])}const y=p(g,[["render",c],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/vehicles/psacc/vehicle.vue"]]);export{y as default};