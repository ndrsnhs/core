import{C as r}from"./HardwareInstallation-a0083e3a.js";import{_ as a,u as t,k as l,l as u,D as n,N as c,y as m}from"./vendor-f2b8aa6f.js";import"./vendor-fortawesome-71546160.js";import"./index-b0e5e618.js";import"./vendor-bootstrap-4ad604fa.js";import"./vendor-jquery-d3cb8fad.js";import"./vendor-axios-65ecee4b.js";import"./vendor-sortablejs-2f1828d0.js";import"./dynamic-import-helper-be004503.js";const d={name:"DeviceOpenwbEvukitCounter",mixins:[r]},_={class:"device-openwb-evukit-counter"};function v(e,o,f,b,w,x){const i=t("openwb-base-heading"),s=t("openwb-base-select-input");return l(),u("div",_,[n(i,null,{default:c(()=>[m(" Einstellungen für openWB EVU-Kit Zähler ")]),_:1}),n(s,{title:"Zählermodell",notSelected:"Bitte auswählen",options:[{value:3,text:"B23"},{value:1,text:"Lovato"},{value:0,text:"MPM3PM"},{value:2,text:"SDM630/SDM72D-M"}],"model-value":e.component.configuration.version,required:"","onUpdate:modelValue":o[0]||(o[0]=p=>e.updateConfiguration(p,"configuration.version"))},null,8,["model-value"])])}const $=a(d,[["render",v],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/openwb/openwb_evu_kit/counter.vue"]]);export{$ as default};