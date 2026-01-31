/**
 * A2UI Validator Test Runner
 *
 * Simple test runner to verify validation functionality
 */

// Mock the catalog functions
const mockCatalog = {
  'a2ui.StatCard': true,
  'a2ui.Section': true,
  'a2ui.HeadlineCard': true,
  'a2ui.Grid': true,
};

function isComponentRegistered(type) {
  return type in mockCatalog;
}

// Simplified validation logic for testing
function isSerializable(value) {
  if (value === null) return true;
  const type = typeof value;

  if (['string', 'number', 'boolean'].includes(type)) {
    return true;
  }

  if (['function', 'undefined', 'symbol'].includes(type)) {
    return false;
  }

  if (Array.isArray(value)) {
    return value.every(isSerializable);
  }

  if (type === 'object') {
    return Object.values(value).every(isSerializable);
  }

  return false;
}

function validateA2UIComponent(component) {
  const errors = [];
  const warnings = [];

  // Check required field: id
  if (!component.id || typeof component.id !== 'string') {
    errors.push({
      type: 'MISSING_REQUIRED_FIELD',
      message: 'Component must have a valid "id" field (string)',
      path: 'root',
    });
  }

  // Check required field: type
  if (!component.type || typeof component.type !== 'string') {
    errors.push({
      type: 'MISSING_REQUIRED_FIELD',
      message: 'Component must have a valid "type" field (string)',
      path: 'root',
    });
  } else {
    // Check type convention
    if (!component.type.startsWith('a2ui.')) {
      warnings.push({
        type: 'INVALID_TYPE',
        message: `Component type "${component.type}" does not follow a2ui.* naming convention`,
        path: 'root',
      });
    }

    // Check registration
    if (!isComponentRegistered(component.type)) {
      errors.push({
        type: 'UNREGISTERED_TYPE',
        message: `Component type "${component.type}" is not registered in the catalog`,
        path: 'root',
      });
    }
  }

  // Check required field: props
  if (component.props === undefined || component.props === null) {
    errors.push({
      type: 'MISSING_REQUIRED_FIELD',
      message: 'Component must have a "props" field',
      path: 'root',
    });
  } else if (typeof component.props !== 'object' || Array.isArray(component.props)) {
    errors.push({
      type: 'INVALID_PROPS',
      message: 'Component "props" must be an object',
      path: 'root',
    });
  } else {
    // Check serializable props
    for (const [key, value] of Object.entries(component.props)) {
      if (!isSerializable(value)) {
        errors.push({
          type: 'NON_SERIALIZABLE_PROP',
          message: `Prop "${key}" contains non-serializable value`,
          path: `root.props.${key}`,
        });
      }
    }
  }

  return {
    valid: errors.length === 0,
    errors,
    warnings,
    stats: {
      totalComponents: 1,
      uniqueTypes: new Set([component.type]),
      maxDepth: 0,
      totalProps: component.props ? Object.keys(component.props).length : 0,
    },
  };
}

// Test cases
const tests = [
  {
    name: 'Valid Simple Component',
    component: {
      id: 'test-1',
      type: 'a2ui.StatCard',
      props: { label: 'Users', value: '1234' },
    },
    expectedValid: true,
  },
  {
    name: 'Missing Type Field',
    component: {
      id: 'test-2',
      props: { label: 'Missing Type', value: '100' },
    },
    expectedValid: false,
  },
  {
    name: 'Missing ID Field',
    component: {
      type: 'a2ui.StatCard',
      props: { label: 'Missing ID', value: '100' },
    },
    expectedValid: false,
  },
  {
    name: 'Non-Serializable Props',
    component: {
      id: 'test-3',
      type: 'a2ui.StatCard',
      props: {
        label: 'Test',
        onClick: () => {}, // Function not allowed
      },
    },
    expectedValid: false,
  },
  {
    name: 'Unregistered Type',
    component: {
      id: 'test-4',
      type: 'a2ui.NonExistentComponent',
      props: {},
    },
    expectedValid: false,
  },
  {
    name: 'Null Props Allowed',
    component: {
      id: 'test-5',
      type: 'a2ui.StatCard',
      props: { label: 'Test', value: null },
    },
    expectedValid: true,
  },
];

// Run tests
console.log('========================================');
console.log('A2UI Validator Test Suite');
console.log('========================================\n');

let passed = 0;
let failed = 0;

tests.forEach((test, index) => {
  const result = validateA2UIComponent(test.component);
  const testPassed = result.valid === test.expectedValid;

  if (testPassed) {
    console.log(`✓ Test ${index + 1}: ${test.name}`);
    passed++;
  } else {
    console.log(`✗ Test ${index + 1}: ${test.name}`);
    console.log(`  Expected valid: ${test.expectedValid}, Got: ${result.valid}`);
    if (result.errors.length > 0) {
      console.log('  Errors:', result.errors.map(e => e.message));
    }
    failed++;
  }
});

console.log('\n========================================');
console.log(`Results: ${passed} passed, ${failed} failed`);
console.log('========================================');

// Exit with error code if any tests failed
process.exit(failed > 0 ? 1 : 0);
