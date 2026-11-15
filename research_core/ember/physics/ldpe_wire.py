from __future__ import annotations
import math
from ember.physics.base import PhysicsAdapter
from ember.schemas import ApplicabilityReport,ApplicabilityStatus,CombustionScenario,PhysicsFingerprint,InverseDesignResult,EvidenceLevel
from ember.normalization import canonical_material,canonical_geometry

class LDPEWireP2GAdapter(PhysicsAdapter):
    model_id='ldpe_wire_p2g_similitude_v2'
    title='LDPE insulated wire pressure-gravity similitude bridge'
    SOURCE='https://doi.org/10.1016/j.proci.2024.105766'
    VALID=[('CU',0.15,0.15),('NICR',0.15,0.15),('CU',0.25,0.15),('NICR',0.25,0.15),('CU',0.25,0.30),('NICR',0.25,0.30)]
    @staticmethod
    def invariant(P,g): return P*P*g
    def _config_ok(self,s):
        if not s.core_material or s.core_radius_mm is None or s.insulation_thickness_mm is None:return False
        cm=s.core_material.strip().upper().replace('-','')
        return any(cm==a and abs(s.core_radius_mm-b)<1e-6 and abs(s.insulation_thickness_mm-c)<1e-6 for a,b,c in self.VALID)
    def applicability(self,s):
        checks={'material_ldpe':canonical_material(s.material)=='LDPE','wire_geometry':canonical_geometry(s.geometry)=='WIRE_OPPOSED','validated_wire_configuration':self._config_ok(s),'oxygen_near_21pct':0.20<=s.oxygen_fraction<=0.22,'pressure_18_101kpa':18<=s.pressure_kpa<=101.325,'positive_gravity':s.gravity_g>0,'low_or_quiescent_flow':s.forced_flow_m_s is None or 0<=s.forced_flow_m_s<=0.06}
        core=checks['material_ldpe'] and checks['wire_geometry'] and checks['validated_wire_configuration']
        strict=core and checks['oxygen_near_21pct'] and checks['pressure_18_101kpa'] and checks['positive_gravity'] and checks['low_or_quiescent_flow']
        status=ApplicabilityStatus.EXTRAPOLATED_PHYSICS if strict else ApplicabilityStatus.PARTIAL if core else ApplicabilityStatus.OUT_OF_DOMAIN
        warns=['P²g is a pressure-gravity similitude approximation; it does not guarantee identical flame-spread rate or chemistry.']
        if not checks['validated_wire_configuration']: warns.append('Wire core material/radius/insulation thickness must match an audited configuration.')
        if s.gravity_g<=0: warns.append('No finite-pressure 1-g surrogate exists for exact zero gravity under P²g invariance.')
        if not checks['low_or_quiescent_flow']: warns.append('Flow exceeds the conservative v2 envelope; the implemented P²g bridge does not model arbitrary forced-flow effects.')
        return ApplicabilityReport(status=status,model_id=self.model_id,checks=checks,warnings=warns,rationale='Restricted LDPE-insulated Cu/NiCr wire similitude; core conduction and finite-rate chemistry can break similarity.')
    def fingerprint(self,s):
        app=self.applicability(s); vals={'gravity_g':s.gravity_g,'pressure_kpa':s.pressure_kpa,'oxygen_fraction':s.oxygen_fraction,'p2g_kpa2_g':self.invariant(s.pressure_kpa,s.gravity_g)}
        return PhysicsFingerprint(model_id=self.model_id,values=vals,applicability=app,provenance=[{'source_id':'LDPE_WIRE_P2G_2024','level':EvidenceLevel.PHYSICS_DERIVED.value,'claim':'Pressure-gravity similitude uses P²g as the matched quantity under stated assumptions.','url':self.SOURCE,'note':'Configuration-specific and not a universal wire-fire law.'}])
    def inverse_design(self,target,test_gravity_g=1.0,strict_domain=True,optimize_flow=True):
        tf=self.fingerprint(target)
        if tf.applicability.status==ApplicabilityStatus.OUT_OF_DOMAIN or (strict_domain and tf.applicability.status==ApplicabilityStatus.PARTIAL) or target.gravity_g<=0 or test_gravity_g<=0:
            return InverseDesignResult(model_id=self.model_id,status=ApplicabilityStatus.NO_VALIDATED_BRIDGE,target_applicability_status=tf.applicability.status,target_fingerprint=tf.values,proposed_scenario=None,proposed_fingerprint=None,objective_value=None,warnings=tf.applicability.warnings,provenance=tf.provenance)
        P=target.pressure_kpa*math.sqrt(target.gravity_g/test_gravity_g)
        proposed=target.model_copy(update={'gravity_g':test_gravity_g,'pressure_kpa':P,'notes':'P²g-matched LDPE wire surrogate; not full flame equivalence.'})
        pf=self.fingerprint(proposed)
        rel=(pf.values['p2g_kpa2_g']-tf.values['p2g_kpa2_g'])/tf.values['p2g_kpa2_g']
        status=ApplicabilityStatus.EXTRAPOLATED_PHYSICS
        if strict_domain and not (18<=P<=101.325): status=ApplicabilityStatus.NO_VALIDATED_BRIDGE
        return InverseDesignResult(model_id=self.model_id,status=status,target_applicability_status=tf.applicability.status,proposed_applicability_status=pf.applicability.status,target_fingerprint=tf.values,proposed_scenario=proposed,proposed_fingerprint=pf.values,objective_value=rel*rel,residuals={'p2g_relative':rel},unmatched_physics={'not_modeled':['finite-rate chemistry','core-conduction differences beyond audited configuration','molten polymer motion/dripping','radiation and detailed flame structure']},warnings=tf.applicability.warnings+pf.applicability.warnings,provenance=tf.provenance)
