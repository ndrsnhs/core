import{V as a}from"./VehicleConfig-668eeb31.js";import{_ as s,u as p,k as u,l as m,G as n,E as r,y as l}from"./vendor-88a3d381.js";import"./vendor-fortawesome-2ab93053.js";import"./index-d7731c53.js";import"./vendor-bootstrap-6598ffd1.js";import"./vendor-jquery-536f4487.js";import"./vendor-axios-29ac7e52.js";import"./vendor-sortablejs-f1eda7cf.js";import"./dynamic-import-helper-be004503.js";const d={name:"VehicleSocHttp",mixins:[a]},c={class:"vehicle-soc-http"};function v(t,e,f,h,g,w){const i=p("openwb-base-text-input");return u(),m("div",c,[n(i,{title:"SoC URL",subtype:"url",required:"","model-value":t.vehicle.configuration.soc_url,"onUpdate:modelValue":e[0]||(e[0]=o=>t.updateConfiguration(o,"configuration.soc_url"))},{help:r(()=>e[2]||(e[2]=[l(" Es wird vom Server eine Zahl (Float mit Punkt als Dezimaltrennzeichen oder Integer) erwartet, welche den aktuellen Ladestand in Prozent (0 bis 100) zurückgibt. ")])),_:1},8,["model-value"]),n(i,{title:"Reichweiten URL",subtype:"url","model-value":t.vehicle.configuration.range_url,"onUpdate:modelValue":e[1]||(e[1]=o=>t.updateConfiguration(o,"configuration.range_url"))},{help:r(()=>e[3]||(e[3]=[l(" Es wird vom Server eine Zahl (Float mit Punkt als Dezimaltrennzeichen oder Integer) erwartet, welche die aktuelle Reichweite in Kilometern darstellt. Diese Angabe ist optional. ")])),_:1},8,["model-value"])])}const S=s(d,[["render",v],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/vehicles/http/vehicle.vue"]]);export{S as default};