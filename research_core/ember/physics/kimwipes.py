from __future__ import annotations
import math
from ember.physics.base import PhysicsAdapter
from ember.schemas import ApplicabilityReport,ApplicabilityStatus,CombustionScenario,PhysicsFingerprint,InverseDesignResult,EvidenceLevel
from ember.normalization import canonical_material,canonical_geometry,is_microgravity

class KimwipesConcurrentAdapter(PhysicsAdapter):
    model_id='kimwipes_concurrent_empirical_v2'
    title='Kimwipes concurrent microgravity empirical flame-spread model'
    SOURCE='https://ntrs.nasa.gov/citations/20080034883'
    def applicability(self,s):
        p_psia=s.pressure_kpa/6.894757293168
        checks={'material_kimwipes':canonical_material(s.material)=='KIMWIPES','thin_sheet_concurrent':canonical_geometry(s.geometry)=='THIN_SHEET_CONCURRENT','microgravity_only':is_microgravity(s.gravity_g),'oxygen_24_50pct':0.24<=s.oxygen_fraction<=0.50,'flow_1_30cm_s':s.forced_flow_m_s is not None and 0.01<=s.forced_flow_m_s<=0.30,'pressure_5_14_7psia':5<=p_psia<=14.7}
        core=checks['material_kimwipes'] and checks['thin_sheet_concurrent'] and s.forced_flow_m_s is not None
        strict=core and all(checks[k] for k in ['microgravity_only','oxygen_24_50pct','flow_1_30cm_s','pressure_5_14_7psia'])
        status=ApplicabilityStatus.IN_DOMAIN if strict else ApplicabilityStatus.PARTIAL if core else ApplicabilityStatus.OUT_OF_DOMAIN
        warns=[]
        if not checks['microgravity_only']: warns.append('Published v2 empirical regression is microgravity-specific; no partial-gravity interpolation is performed.')
        warns.append('Near extinction, the published concurrent data fall below the linear fit; predictions are research estimates, not safety limits.')
        return ApplicabilityReport(status=status,model_id=self.model_id,checks=checks,warnings=warns,rationale='NASA empirical concurrent-spread correlation with x=X_O2*U(cm/s)*sqrt(P(atm)); opposed-flow behavior is deliberately excluded.')
    def fingerprint(self,s):
        app=self.applicability(s); vals={'gravity_g':s.gravity_g,'pressure_kpa':s.pressure_kpa,'oxygen_fraction':s.oxygen_fraction}
        prov=[{'source_id':'NASA_TM_2008_215260_KIMWIPES','level':EvidenceLevel.NASA_EMPIRICAL_CORRELATION.value,'claim':'Concurrent Kimwipes flame-spread correlation: y=0.2498x+0.4038 (R²=0.97); power fit y=0.6763x^0.6187 (R²=0.93).','url':self.SOURCE,'note':'x uses O2 mole fraction, flow cm/s, and sqrt(pressure atm).'}]
        if app.status!=ApplicabilityStatus.OUT_OF_DOMAIN and s.forced_flow_m_s is not None:
            x=s.oxygen_fraction*(s.forced_flow_m_s*100)*(s.pressure_kpa/101.325)**0.5
            vals.update({'correlation_x':x,'spread_linear_cm_s':0.2498*x+0.4038,'spread_power_cm_s':0.6763*(x**0.6187)})
        return PhysicsFingerprint(model_id=self.model_id,values=vals,applicability=app,provenance=prov)
    def inverse_design(self,target,test_gravity_g=1.0,strict_domain=True,optimize_flow=True):
        tf=self.fingerprint(target)
        return InverseDesignResult(model_id=self.model_id,status=ApplicabilityStatus.NO_VALIDATED_BRIDGE,target_applicability_status=tf.applicability.status,target_fingerprint=tf.values,proposed_scenario=None,proposed_fingerprint=None,objective_value=None,unmatched_physics={'reason':'Empirical microgravity spread-rate model is not a validated gravity bridge.'},warnings=tf.applicability.warnings+['EMBER v2 deliberately abstains from inverting this empirical correlation across gravity.'],provenance=tf.provenance)
