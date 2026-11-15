from __future__ import annotations
from ember.physics.base import PhysicsAdapter
from ember.schemas import ApplicabilityReport,ApplicabilityStatus,CombustionScenario,PhysicsFingerprint,InverseDesignResult,EvidenceLevel
from ember.normalization import canonical_material,canonical_geometry,is_earth_gravity

class ThinPMMANCAAdapter(PhysicsAdapter):
    model_id='thin_pmma_nca_analog_v2'
    title='Thin PMMA Narrow Channel Apparatus microgravity analog'
    SOURCE='https://ntrs.nasa.gov/citations/20140004923'
    def applicability(self,s):
        checks={'material_pmma':canonical_material(s.material)=='PMMA','thin_sheet_opposed_nca':canonical_geometry(s.geometry)=='THIN_SHEET_OPPOSED_NCA','earth_test':is_earth_gravity(s.gravity_g),'pressure_near_1atm':95<=s.pressure_kpa<=105,'thickness_50_or_75um':s.thickness_mm is not None and (abs(s.thickness_mm-.05)<1e-6 or abs(s.thickness_mm-.075)<1e-6),'oxygen_21_30_50pct':any(abs(s.oxygen_fraction-x)<0.005 for x in (.21,.30,.50)),'flow_3_35cm_s':s.forced_flow_m_s is not None and .03<=s.forced_flow_m_s<=.35,'channel_gap_present':s.channel_gap_mm is not None and s.channel_gap_mm>0}
        core=checks['material_pmma'] and checks['thin_sheet_opposed_nca'] and checks['channel_gap_present']
        strict=core and all(checks[k] for k in ['earth_test','pressure_near_1atm','thickness_50_or_75um','oxygen_21_30_50pct','flow_3_35cm_s'])
        status=ApplicabilityStatus.IN_DOMAIN if strict else ApplicabilityStatus.PARTIAL if core else ApplicabilityStatus.OUT_OF_DOMAIN
        warns=['NCA is an Earth-based apparatus analog that suppresses buoyancy; it is not a pressure↔gravity equivalence equation.','Wall heat loss becomes important near extinction and depends on channel gap.']
        return ApplicabilityReport(status=status,model_id=self.model_id,checks=checks,warnings=warns,rationale='Validated as an apparatus analog for thin PMMA opposed-flow microgravity behavior at tested 1-atm configurations.')
    def fingerprint(self,s):
        app=self.applicability(s); vals={'gravity_g':s.gravity_g,'pressure_kpa':s.pressure_kpa,'oxygen_fraction':s.oxygen_fraction,'forced_flow_m_s':s.forced_flow_m_s or 0,'thickness_mm':s.thickness_mm or 0,'channel_gap_mm':s.channel_gap_mm or 0,'analog_target_microgravity':1.0}
        return PhysicsFingerprint(model_id=self.model_id,values=vals,applicability=app,provenance=[{'source_id':'NASA_NTRS_20140004923','level':EvidenceLevel.NASA_OBSERVED.value,'claim':'NCA thin-PMMA tests at 1 atm, 3–35 cm/s, 21/30/50% O2, 50/75 µm were compared with actual microgravity and successfully reproduced spread behavior in the tested range.','url':self.SOURCE,'note':'Apparatus analog; no universal gravity mapping.'}])
    def inverse_design(self,target,test_gravity_g=1.0,strict_domain=True,optimize_flow=True):
        tf=self.fingerprint(target)
        return InverseDesignResult(model_id=self.model_id,status=ApplicabilityStatus.NO_VALIDATED_BRIDGE,target_applicability_status=tf.applicability.status,target_fingerprint=tf.values,proposed_scenario=None,proposed_fingerprint=None,objective_value=None,unmatched_physics={'supported_analog':'Use audited NCA configurations as Earth-based microgravity analog; no inverse pressure/gravity solver is claimed.'},warnings=tf.applicability.warnings,provenance=tf.provenance)
