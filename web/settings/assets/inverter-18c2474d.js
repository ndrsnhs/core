import{C as p}from"./HardwareInstallation-d2c0f1d5.js";import{_ as a,u as n,k as m,l as d,D as t,N as u,y as l}from"./vendor-a21b3a62.js";import"./vendor-fortawesome-41164876.js";import"./index-c79666b6.js";import"./vendor-bootstrap-d0c3645c.js";import"./vendor-jquery-a5dbbab1.js";import"./vendor-axios-0e6de98a.js";import"./vendor-sortablejs-3016fed8.js";import"./dynamic-import-helper-be004503.js";const c={name:"DeviceDeyeInverter",mixins:[p]},_={class:"device-deye-inverter"};function b(o,e,f,v,g,w){const i=n("openwb-base-heading"),r=n("openwb-base-number-input");return m(),d("div",_,[t(i,null,{default:u(()=>e[1]||(e[1]=[l(" Einstellungen für Deye Wechselrichter ")])),_:1}),t(r,{title:"Modbus ID",required:"","model-value":o.component.configuration.modbus_id,min:"1",max:"255","onUpdate:modelValue":e[0]||(e[0]=s=>o.updateConfiguration(s,"configuration.modbus_id"))},null,8,["model-value"])])}const V=a(c,[["render",b],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/deye/deye/inverter.vue"]]);export{V as default};