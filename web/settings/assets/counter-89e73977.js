import{C as d}from"./HardwareInstallation-61d444d7.js";import{_ as u,u as n,k as m,l as c,G as r,E as i,y as o,x as l}from"./vendor-06e11d0e.js";import"./vendor-fortawesome-05d7e447.js";import"./index-3434d31b.js";import"./vendor-bootstrap-4263d7eb.js";import"./vendor-jquery-9fc083b4.js";import"./vendor-axios-22b906fb.js";import"./vendor-sortablejs-0bb60e5b.js";import"./dynamic-import-helper-be004503.js";const f={name:"DeviceDiscovergyCounter",mixins:[d]},g={class:"device-discovergy-counter"};function _(t,e,v,b,w,x){const s=n("openwb-base-heading"),a=n("openwb-base-text-input");return m(),c("div",g,[r(s,null,{default:i(()=>e[1]||(e[1]=[o(" Einstellungen für Discovergy Zähler ")])),_:1}),r(a,{title:"Meter-ID",required:"","model-value":t.component.configuration.meter_id,"onUpdate:modelValue":e[0]||(e[0]=p=>t.updateConfiguration(p,"configuration.meter_id"))},{help:i(()=>e[2]||(e[2]=[o(" Um die ID herauszufinden mit dem Browser die Adresse "),l("a",{href:"https://api.discovergy.com/public/v1/meters",target:"_blank",rel:"noopener noreferrer"}," https://api.discovergy.com/public/v1/meters ",-1),o(" aufrufen und dort Benutzername und Passwort eingeben. Hier wird nun u.a. die ID des Zählers angezeigt. ")])),_:1},8,["model-value"])])}const E=u(f,[["render",_],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/discovergy/discovergy/counter.vue"]]);export{E as default};