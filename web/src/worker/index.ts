import { addTrace } from "./add-trace";
import { health } from "./health";
import { analyzeArtifact } from "./analyze-artifact";

const workers = [health, addTrace, analyzeArtifact];

export default workers;
