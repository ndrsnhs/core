import{C as a}from"./HardwareInstallation-a0083e3a.js";import{_ as u,u as t,k as p,l,D as n,N as c,y as m}from"./vendor-f2b8aa6f.js";import"./vendor-fortawesome-71546160.js";import"./index-b0e5e618.js";import"./vendor-bootstrap-4ad604fa.js";import"./vendor-jquery-d3cb8fad.js";import"./vendor-axios-65ecee4b.js";import"./vendor-sortablejs-2f1828d0.js";import"./dynamic-import-helper-be004503.js";const _={name:"DeviceYoulessInverter",mixins:[a]},d={class:"device-youless-inverter"};function f(e,o,b,v,g,x){const s=t("openwb-base-heading"),i=t("openwb-base-button-group-input");return p(),l("div",d,[n(s,null,{default:c(()=>[m(" Einstellungen für Youless LS120 Wechselrichter ")]),_:1}),n(i,{title:"S0-Eingang auslesen",buttons:[{buttonValue:!1,text:"nein"},{buttonValue:!0,text:"ja"}],"model-value":e.component.configuration.source_s0,"onUpdate:modelValue":o[0]||(o[0]=r=>e.updateConfiguration(r,"configuration.source_s0"))},null,8,["model-value"])])}const N=u(_,[["render",f],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/youless/youless/inverter.vue"]]);export{N as default};