import{C as s}from"./ChargePointInstallation-d3922b37.js";import{_ as p,u as n,k as u,l as m,G as i,E as d,y as l}from"./vendor-06e11d0e.js";import"./vendor-fortawesome-05d7e447.js";import"./index-3434d31b.js";import"./vendor-bootstrap-4263d7eb.js";import"./vendor-jquery-9fc083b4.js";import"./vendor-axios-22b906fb.js";import"./vendor-sortablejs-0bb60e5b.js";import"./dynamic-import-helper-be004503.js";const g={name:"ChargePointSmartwb",mixins:[s]},b={class:"charge-point-smartwb"};function c(t,e,f,_,w,v){const r=n("openwb-base-text-input"),a=n("openwb-base-number-input");return u(),m("div",b,[i(r,{title:"IP oder Hostname",subtype:"host",required:"","model-value":t.chargePoint.configuration.ip_address,"onUpdate:modelValue":e[0]||(e[0]=o=>t.updateConfiguration(o,"configuration.ip_address"))},null,8,["model-value"]),i(a,{title:"Wartezeit",required:"",min:2,max:10,unit:"s","model-value":t.chargePoint.configuration.timeout,"onUpdate:modelValue":e[1]||(e[1]=o=>t.updateConfiguration(o,"configuration.timeout"))},{help:d(()=>e[2]||(e[2]=[l(" Zeitangabe in Sekunden, für die auf eine Antwort des Ladepunktes gewartet wird. Wird diese Zeit überschritten, so wird von einer Kommunikationsstörung ausgegangen. ")])),_:1},8,["model-value"])])}const q=p(g,[["render",c],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/charge_points/smartwb/chargePoint.vue"]]);export{q as default};