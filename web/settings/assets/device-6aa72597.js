import{D as p}from"./HardwareInstallation-d2c0f1d5.js";import{_ as u,u as n,k as m,l as _,D as a,N as i,y as r}from"./vendor-a21b3a62.js";import"./vendor-fortawesome-41164876.js";import"./index-c79666b6.js";import"./vendor-bootstrap-d0c3645c.js";import"./vendor-jquery-a5dbbab1.js";import"./vendor-axios-0e6de98a.js";import"./vendor-sortablejs-3016fed8.js";import"./dynamic-import-helper-be004503.js";const f={name:"DeviceSolarwatt",mixins:[p]},v={class:"device-solarwatt"};function c(t,e,w,b,g,x){const s=n("openwb-base-heading"),l=n("openwb-base-text-input"),d=n("openwb-base-select-input");return m(),_("div",v,[a(s,null,{default:i(()=>e[2]||(e[2]=[r(" Einstellungen für Solarwatt/My Reserve ")])),_:1}),a(l,{title:"IP oder Hostname",subtype:"host",required:"","model-value":t.device.configuration.ip_address,"onUpdate:modelValue":e[0]||(e[0]=o=>t.updateConfiguration(o,"configuration.ip_address"))},null,8,["model-value"]),a(d,{title:"Abrufmethode","not-selected":"Bitte auswählen",options:[{value:0,text:"Gateway"},{value:1,text:"Energy Manager"}],"model-value":t.device.configuration.energy_manager,required:"","onUpdate:modelValue":e[1]||(e[1]=o=>t.updateConfiguration(o,"configuration.energy_manager"))},{help:i(()=>e[3]||(e[3]=[r(" Wenn beide Abrufmethoden verwendet werden sollen, muss für jede Methode ein Gerät erstellt werden. ")])),_:1},8,["model-value"])])}const E=u(f,[["render",c],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/solar_watt/solar_watt/device.vue"]]);export{E as default};